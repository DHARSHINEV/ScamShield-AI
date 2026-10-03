"use client";

import React, { useState, useEffect } from "react";
import { InputTabs, AnalysisMode } from "./InputTabs";
import { AnalysisSequence } from "./AnalysisSequence";
import { RiskGauge } from "./RiskGauge";
import { RiskBreakdown } from "./RiskBreakdown";
import { RedFlagText } from "./RedFlagText";
import { EvidenceCard } from "./EvidenceCard";
import { ActionPlan } from "./ActionPlan";
import { GuardianCard } from "./GuardianCard";
import { 
  analyzeText, 
  analyzeUrl, 
  analyzeImage, 
  analyzeQrCode, 
  analyzeVoice, 
  fetchDemoCases, 
  FullAnalysisResponse, 
  DemoCase 
} from "@/lib/api";
import { AlertCircle, RotateCcw, Sparkles } from "lucide-react";

interface AnalyzerProps {
  currentLanguage: string;
}

export const Analyzer: React.FC<AnalyzerProps> = ({ currentLanguage }) => {
  const [mode, setMode] = useState<AnalysisMode>("message");
  const [textInput, setTextInput] = useState<string>("");
  const [urlInput, setUrlInput] = useState<string>("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [voiceTranscript, setVoiceTranscript] = useState<string>("");
  
  const [demoCases, setDemoCases] = useState<DemoCase[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<FullAnalysisResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    fetchDemoCases().then(setDemoCases).catch(console.error);
  }, []);

  const handleSelectDemo = (demo: DemoCase) => {
    setErrorMessage(null);
    setAnalysisResult(null);
    if (demo.text.startsWith("http://") || demo.text.startsWith("https://")) {
      setMode("url");
      setUrlInput(demo.text);
    } else {
      setMode("message");
      setTextInput(demo.text);
    }
  };

  const handleAnalyze = async () => {
    setIsLoading(true);
    setErrorMessage(null);
    setAnalysisResult(null);

    try {
      let result: FullAnalysisResponse;

      if (mode === "message") {
        result = await analyzeText(textInput, currentLanguage);
      } else if (mode === "url") {
        result = await analyzeUrl(urlInput, currentLanguage);
      } else if (mode === "screenshot") {
        if (!selectedFile) throw new Error("Please select an image file.");
        result = await analyzeImage(selectedFile, currentLanguage);
      } else if (mode === "qr") {
        if (!selectedFile) throw new Error("Please select a QR code image.");
        result = await analyzeQrCode(selectedFile, currentLanguage);
      } else if (mode === "voice") {
        if (!selectedFile && !voiceTranscript) {
          throw new Error("Please select an audio file or enter a voice transcript.");
        }
        if (selectedFile) {
          result = await analyzeVoice(selectedFile, voiceTranscript, currentLanguage);
        } else {
          result = await analyzeText(voiceTranscript, currentLanguage);
        }
      } else {
        throw new Error("Unsupported analysis mode.");
      }

      setAnalysisResult(result);

      // Save to localStorage history
      try {
        const existing = JSON.parse(localStorage.getItem("scamshield_history") || "[]");
        const snippet = (result.sanitized_input || textInput || urlInput || "Screenshot / QR / Audio Scan").slice(0, 100);
        const newEntry = {
          id: "scan-" + Date.now(),
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', day: '2-digit', month: 'short' }),
          snippet: snippet,
          classification: result.classification,
          percentage: result.percentage,
          scamType: result.scam_type
        };
        const updated = [newEntry, ...existing.slice(0, 19)];
        localStorage.setItem("scamshield_history", JSON.stringify(updated));
      } catch (e) {
        console.error("Failed saving history", e);
      }

    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : "Analysis request failed. Please check inputs.";
      setErrorMessage(errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setErrorMessage(null);
    setTextInput("");
    setUrlInput("");
    setSelectedFile(null);
    setVoiceTranscript("");
  };

  // Localized explanation banner
  const localizedInfo = analysisResult?.multilingual[currentLanguage] || analysisResult?.multilingual["en"];

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      
      {/* Input Section */}
      <InputTabs
        mode={mode}
        setMode={setMode}
        textInput={textInput}
        setTextInput={setTextInput}
        urlInput={urlInput}
        setUrlInput={setUrlInput}
        selectedFile={selectedFile}
        setSelectedFile={setSelectedFile}
        voiceTranscript={voiceTranscript}
        setVoiceTranscript={setVoiceTranscript}
        demoCases={demoCases}
        onSelectDemo={handleSelectDemo}
        onAnalyze={handleAnalyze}
        isLoading={isLoading}
      />

      {/* Error Message */}
      {errorMessage && (
        <div className="glass-card p-4 rounded-2xl border border-red-500/40 bg-red-950/20 text-red-300 text-xs flex items-center space-x-3 animate-fadeIn">
          <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Progressive Scanning Animation */}
      {isLoading && <AnalysisSequence />}

      {/* Complete Results Display */}
      {analysisResult && !isLoading && (
        <div className="space-y-8 animate-fadeIn">
          
          {/* Top Results Bar */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-extrabold text-white tracking-tight">
                  Security Intelligence Assessment
                </span>
                <span className="text-xs px-2.5 py-0.5 rounded-full font-mono bg-slate-800 text-slate-300">
                  {analysisResult.analysis_metadata.latency_ms} ms
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Engine: Multi-Signal Fusion (Rules + Lexical Heuristics + ML Classifier)
              </p>
            </div>

            <button
              onClick={handleReset}
              className="self-start sm:self-auto px-3.5 py-1.5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Analyze Another</span>
            </button>
          </div>

          {/* Multilingual Localized Executive Summary Banner */}
          {localizedInfo && (
            <div className="p-4 rounded-2xl bg-cyan-950/20 border border-cyan-500/30 flex items-start space-x-3">
              <Sparkles className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />
              <div className="text-xs">
                <span className="font-bold text-cyan-300 uppercase tracking-wider block mb-1">
                  Executive Explanation ({localizedInfo.language}):
                </span>
                <p className="text-slate-200 text-sm leading-relaxed font-sans">
                  {localizedInfo.summary}
                </p>
              </div>
            </div>
          )}

          {/* Gauge and Breakdown Row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-1">
              <RiskGauge
                score={analysisResult.risk_score}
                percentage={analysisResult.percentage}
                classification={analysisResult.classification}
                scamType={analysisResult.scam_type}
              />
            </div>
            <div className="md:col-span-2">
              <RiskBreakdown breakdown={analysisResult.risk_breakdown} />
            </div>
          </div>

          {/* Red Flag Text Highlighting */}
          <RedFlagText
            originalText={analysisResult.sanitized_input || textInput || urlInput}
            redFlags={analysisResult.red_flags}
          />

          {/* TrustLens Evidence Engine */}
          <EvidenceCard
            cards={analysisResult.evidence_cards}
            classification={analysisResult.classification}
          />

          {/* Concrete Action Plan & Family Guardian */}
          <ActionPlan
            actionPlan={analysisResult.action_plan}
            classification={analysisResult.classification}
          />

          {/* Family Guardian Trigger */}
          <div className="glass-panel p-6 rounded-2xl border border-red-500/30 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h4 className="text-sm font-bold text-white">
                Protect Loved Ones from this Attack Wave
              </h4>
              <p className="text-xs text-slate-400 mt-0.5">
                Generate an easy-to-read, one-click alert formatted for family WhatsApp groups or SMS.
              </p>
            </div>
            <GuardianCard
              messageSnippet={analysisResult.sanitized_input || textInput}
              riskLevel={analysisResult.classification}
              scamType={analysisResult.scam_type}
              language={currentLanguage}
            />
          </div>

        </div>
      )}

    </div>
  );
};
