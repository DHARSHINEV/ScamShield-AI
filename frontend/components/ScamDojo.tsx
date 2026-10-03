"use client";

import React, { useState, useEffect } from "react";
import confetti from "canvas-confetti";
import { 
  Trophy, 
  Flame, 
  Target, 
  CheckCircle2, 
  XCircle, 
  ArrowRight, 
  Award, 
  ShieldAlert, 
  ShieldCheck, 
  RefreshCw,
  Lightbulb
} from "lucide-react";
import { fetchDojoChallenges, submitDojoAnswer, DojoChallenge, DojoAnswerResponse } from "@/lib/api";

export const ScamDojo: React.FC = () => {
  const [challenges, setChallenges] = useState<DojoChallenge[]>([]);
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(true);
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [lastResponse, setLastResponse] = useState<DojoAnswerResponse | null>(null);

  // Game Stats
  const [streak, setStreak] = useState<number>(0);
  const [score, setScore] = useState<number>(0);
  const [totalCorrect, setTotalCorrect] = useState<number>(0);
  const [totalAnswered, setTotalAnswered] = useState<number>(0);
  const [skillLevel, setSkillLevel] = useState<string>("Vigilant Rookie");

  useEffect(() => {
    // Load local storage if present
    const savedScore = localStorage.getItem("scamshield_dojo_score");
    const savedStreak = localStorage.getItem("scamshield_dojo_streak");
    const savedTotal = localStorage.getItem("scamshield_dojo_total");
    const savedCorrect = localStorage.getItem("scamshield_dojo_correct");
    if (savedScore) setScore(parseInt(savedScore, 10));
    if (savedStreak) setStreak(parseInt(savedStreak, 10));
    if (savedTotal) setTotalAnswered(parseInt(savedTotal, 10));
    if (savedCorrect) setTotalCorrect(parseInt(savedCorrect, 10));

    fetchDojoChallenges()
      .then((data) => {
        setChallenges(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Dojo challenges load failed", err);
        setLoading(false);
      });
  }, []);

  const handleChoice = async (choice: "SAFE" | "SUSPICIOUS") => {
    if (submitting || lastResponse || challenges.length === 0) return;
    setSubmitting(true);
    const challenge = challenges[currentIndex];

    try {
      const res = await submitDojoAnswer(
        challenge.id,
        choice,
        streak,
        totalAnswered,
        totalCorrect
      );
      setLastResponse(res);
      setStreak(res.updated_streak);
      setScore((prev) => prev + res.updated_score);
      setTotalCorrect(res.updated_correct);
      setTotalAnswered(res.total_answered);
      setSkillLevel(res.skill_level);

      // Save to localStorage
      localStorage.setItem("scamshield_dojo_score", (score + res.updated_score).toString());
      localStorage.setItem("scamshield_dojo_streak", res.updated_streak.toString());
      localStorage.setItem("scamshield_dojo_total", res.total_answered.toString());
      localStorage.setItem("scamshield_dojo_correct", res.updated_correct.toString());

      if (res.is_correct) {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.6 }
        });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleNextChallenge = () => {
    setLastResponse(null);
    if (currentIndex < challenges.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      // Loop or shuffle
      setCurrentIndex(0);
    }
  };

  if (loading) {
    return (
      <div className="glass-panel p-12 rounded-3xl border border-slate-800 text-center text-slate-400 font-mono">
        🥋 Initializing Scam Dojo scenarios...
      </div>
    );
  }

  if (challenges.length === 0) {
    return (
      <div className="glass-panel p-12 rounded-3xl border border-slate-800 text-center text-slate-400 font-mono">
        Scam Dojo scenarios unavailable. Ensure backend server is running.
      </div>
    );
  }

  const currentChallenge = challenges[currentIndex];
  const accuracy = totalAnswered > 0 ? Math.round((totalCorrect / totalAnswered) * 100) : 100;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Dojo Header & Stats Banner */}
      <div className="glass-panel p-6 rounded-3xl border border-purple-500/30 relative overflow-hidden shadow-2xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🥋</span>
              <h2 className="text-2xl font-extrabold text-white tracking-tight">
                SCAM DOJO
              </h2>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 border border-purple-500/30 font-semibold">
                Interactive Training
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-1">
              Train yourself to spot scams before they become real. 6 difficulty levels, real attack vectors.
            </p>
          </div>

          {/* Gamification Stats */}
          <div className="flex items-center space-x-3 bg-slate-900/80 p-2 rounded-2xl border border-slate-800">
            {/* Score */}
            <div className="px-3 py-1 text-center">
              <div className="flex items-center justify-center space-x-1 text-amber-400">
                <Trophy className="w-3.5 h-3.5" />
                <span className="font-mono font-bold text-sm">{score}</span>
              </div>
              <div className="text-[10px] text-slate-400 uppercase font-semibold">Points</div>
            </div>

            <div className="h-6 w-px bg-slate-800" />

            {/* Streak */}
            <div className="px-3 py-1 text-center">
              <div className="flex items-center justify-center space-x-1 text-orange-400">
                <Flame className="w-3.5 h-3.5" />
                <span className="font-mono font-bold text-sm">{streak}</span>
              </div>
              <div className="text-[10px] text-slate-400 uppercase font-semibold">Streak</div>
            </div>

            <div className="h-6 w-px bg-slate-800" />

            {/* Accuracy */}
            <div className="px-3 py-1 text-center">
              <div className="flex items-center justify-center space-x-1 text-emerald-400">
                <Target className="w-3.5 h-3.5" />
                <span className="font-mono font-bold text-sm">{accuracy}%</span>
              </div>
              <div className="text-[10px] text-slate-400 uppercase font-semibold">Accuracy</div>
            </div>

            <div className="h-6 w-px bg-slate-800" />

            {/* Rank */}
            <div className="px-3 py-1 text-center">
              <div className="flex items-center justify-center space-x-1 text-purple-400">
                <Award className="w-3.5 h-3.5" />
                <span className="font-bold text-xs truncate max-w-[100px]">{skillLevel.split(" ")[0]}</span>
              </div>
              <div className="text-[10px] text-slate-400 uppercase font-semibold">Rank</div>
            </div>
          </div>
        </div>
      </div>

      {/* Challenge Card */}
      <div className="glass-card p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-xl space-y-6">
        
        {/* Level and Category Bar */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-1 rounded-lg text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30">
              {currentChallenge.level_title}
            </span>
            <span className="text-xs px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 font-semibold capitalize">
              {currentChallenge.category}
            </span>
          </div>

          <span className="text-xs font-mono text-slate-400">
            Challenge {currentIndex + 1} of {challenges.length}
          </span>
        </div>

        {/* Scenario description */}
        <div className="text-xs text-slate-400 italic">
          Scenario: {currentChallenge.scenario}
        </div>

        {/* Message Container */}
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-700/80 font-mono text-sm text-slate-100 leading-relaxed shadow-inner">
          {currentChallenge.message}
        </div>

        {/* Optional URL */}
        {currentChallenge.url && (
          <div className="text-xs text-slate-400 flex items-center space-x-2 font-mono bg-slate-950/60 p-2.5 rounded-xl border border-slate-800">
            <span className="text-cyan-400 font-bold">Link:</span>
            <span className="text-slate-300 truncate">{currentChallenge.url}</span>
          </div>
        )}

        {/* Action Buttons (Before answering) */}
        {!lastResponse && (
          <div className="pt-2 flex flex-col sm:flex-row gap-4">
            <button
              onClick={() => handleChoice("SAFE")}
              disabled={submitting}
              className="flex-1 py-3.5 px-6 rounded-2xl font-bold text-sm bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/40 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <span>It&apos;s SAFE</span>
            </button>

            <button
              onClick={() => handleChoice("SUSPICIOUS")}
              disabled={submitting}
              className="flex-1 py-3.5 px-6 rounded-2xl font-bold text-sm bg-red-600/20 hover:bg-red-600/30 text-red-300 border border-red-500/40 flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 active:translate-y-0"
            >
              <ShieldAlert className="w-5 h-5 text-red-400" />
              <span>It&apos;s SUSPICIOUS / SCAM</span>
            </button>
          </div>
        )}

        {/* Feedback Section (After answering) */}
        {lastResponse && (
          <div className={`p-6 rounded-2xl border space-y-4 animate-fadeIn ${
            lastResponse.is_correct
              ? "bg-emerald-950/20 border-emerald-500/40"
              : "bg-red-950/20 border-red-500/40"
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2.5">
                {lastResponse.is_correct ? (
                  <CheckCircle2 className="w-6 h-6 text-emerald-400" />
                ) : (
                  <XCircle className="w-6 h-6 text-red-400" />
                )}
                <div>
                  <h4 className="text-base font-extrabold text-white">
                    {lastResponse.is_correct ? "CORRECT!" : "INCORRECT"}
                  </h4>
                  <p className="text-xs text-slate-300">
                    This communication is legitimately{" "}
                    <span className="font-bold uppercase text-white font-mono">
                      {lastResponse.correct_classification}
                    </span>.
                  </p>
                </div>
              </div>

              {lastResponse.is_correct && (
                <div className="text-right">
                  <div className="font-mono text-sm font-bold text-emerald-400">
                    +{lastResponse.updated_score} pts
                  </div>
                  <div className="text-[10px] text-slate-400 uppercase">Streak Bonus</div>
                </div>
              )}
            </div>

            {/* Itemized Evidence Bullet points */}
            <div className="space-y-2 pt-2 border-t border-slate-800">
              <div className="text-xs font-bold text-slate-200">
                Why was this the right answer?
              </div>
              {lastResponse.explanation.map((item, idx) => (
                <div key={idx} className="text-xs text-slate-300 flex items-start space-x-2">
                  <span className="text-cyan-400 font-bold shrink-0">✓</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>

            {/* Key Takeaway */}
            <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start space-x-2.5">
              <Lightbulb className="w-4 h-4 text-amber-400 mt-0.5 shrink-0" />
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-300">
                  Key Security Takeaway
                </span>
                <p className="text-xs text-slate-200 mt-0.5">
                  {lastResponse.key_takeaway}
                </p>
              </div>
            </div>

            {/* Next Challenge CTA */}
            <div className="pt-2 text-right">
              <button
                onClick={handleNextChallenge}
                className="px-6 py-2.5 rounded-xl font-bold text-xs bg-purple-600 hover:bg-purple-500 text-white flex items-center space-x-2 inline-flex transition-colors shadow-lg shadow-purple-600/30"
              >
                <span>Next Scenario</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
};
