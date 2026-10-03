"use client";

import React, { useState } from "react";
import { Header } from "@/components/Header";
import { Hero } from "@/components/Hero";
import { Analyzer } from "@/components/Analyzer";
import { ScamDojo } from "@/components/ScamDojo";
import { Dashboard } from "@/components/Dashboard";
import { PrivacySection } from "@/components/PrivacySection";
import { HowItWorks } from "@/components/HowItWorks";
import { Footer } from "@/components/Footer";

export default function Home() {
  const [currentLanguage, setCurrentLanguage] = useState<string>("en");
  const [activeTab, setActiveTab] = useState<string>("analyzer");

  return (
    <div className="min-h-screen flex flex-col bg-[#070B14] text-slate-100 selection:bg-cyan-500/30 selection:text-cyan-200">
      
      {/* Global Header */}
      <Header
        currentLanguage={currentLanguage}
        onLanguageChange={setCurrentLanguage}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <main className="flex-1">
        {/* Landing Hero */}
        <Hero
          onAnalyzeClick={() => setActiveTab("analyzer")}
          onDojoClick={() => setActiveTab("dojo")}
          onHowItWorksClick={() => setActiveTab("how-it-works")}
        />

        {/* Dynamic Main Workspace Tabs */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-12">
          {activeTab === "analyzer" && (
            <>
              <Analyzer currentLanguage={currentLanguage} />
              <div className="pt-10 border-t border-slate-800/80">
                <HowItWorks />
              </div>
            </>
          )}

          {activeTab === "how-it-works" && (
            <HowItWorks />
          )}

          {activeTab === "dojo" && (
            <ScamDojo />
          )}

          {activeTab === "dashboard" && (
            <Dashboard />
          )}

          {activeTab === "privacy" && (
            <PrivacySection />
          )}
        </div>
      </main>

      {/* Global Footer */}
      <Footer />

    </div>
  );
}
