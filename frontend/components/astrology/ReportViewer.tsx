import React, { useState } from 'react';
import { ScoreDial } from './ScoreDial';

export interface PredictionDomain {
  domain: string;
  event_type: string;
  score: number;
  quality_score?: number;
  prediction_strength: string;
  summary: string;
  supporting_factors?: string[];
  manifestations?: string[];
  practical_actions?: string[];
}

export interface ReportViewerProps {
  reportMarkdown?: string;
  predictions?: PredictionDomain[];
  onLanguageChange?: (langCode: string) => void;
}

export const ReportViewer: React.FC<ReportViewerProps> = ({
  reportMarkdown,
  predictions = [],
  onLanguageChange
}) => {
  const [selectedLang, setSelectedLang] = useState<string>('en');
  const [openDomainIdx, setOpenDomainIdx] = useState<number | null>(0);

  const handleLangSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const code = e.target.value;
    setSelectedLang(code);
    if (onLanguageChange) {
      onLanguageChange(code);
    }
  };

  const toggleAccordion = (idx: number) => {
    setOpenDomainIdx(openDomainIdx === idx ? null : idx);
  };

  return (
    <div className="backdrop-blur-md bg-slate-900/60 border border-slate-800/80 shadow-2xl rounded-2xl p-6 text-white space-y-6">
      {/* Header & Language Localizer Selector */}
      <div className="flex flex-wrap justify-between items-center gap-4 border-b border-slate-800 pb-4">
        <div>
          <h2 className="text-2xl font-bold font-serif text-amber-400">Astrological Intelligence Report</h2>
          <p className="text-xs text-slate-400 font-mono">3-Pass DAG Synthesis • Zero-Null Hydration Guard</p>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="lang-select" className="text-xs text-slate-300 font-mono">Language / भाषा / ഭാഷ:</label>
          <select
            id="lang-select"
            value={selectedLang}
            onChange={handleLangSelect}
            className="bg-slate-800 text-amber-400 border border-amber-500/30 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:border-amber-400"
          >
            <option value="en">English (English)</option>
            <option value="hi">हिंदी (Hindi)</option>
            <option value="ta">தமிழ் (Tamil)</option>
            <option value="ml">മലയാളം (Malayalam)</option>
            <option value="es">Español (Spanish)</option>
          </select>
        </div>
      </div>

      {/* Domain Score Dials Highlights Row */}
      {predictions.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3 p-4 bg-slate-800/30 rounded-xl border border-slate-800">
          {predictions.slice(0, 6).map((p, idx) => (
            <ScoreDial key={idx} score={p.score} label={p.domain} size={90} />
          ))}
        </div>
      )}

      {/* Accordion Domain Sections */}
      {predictions.length > 0 ? (
        <div className="space-y-3">
          <h3 className="text-lg font-bold font-serif text-slate-200 mb-2">Confluent Life Domains</h3>
          {predictions.map((p, idx) => {
            const isOpen = openDomainIdx === idx;
            return (
              <div key={idx} className="border border-slate-800 rounded-xl overflow-hidden bg-slate-800/20">
                <button
                  onClick={() => toggleAccordion(idx)}
                  className="w-full p-4 text-left flex justify-between items-center bg-slate-800/40 hover:bg-slate-800/60 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono px-2 py-1 bg-amber-500/10 text-amber-300 rounded border border-amber-500/20">
                      {p.score.toFixed(1)}%
                    </span>
                    <span className="font-bold text-white text-sm">{p.domain}</span>
                    <span className="text-xs text-slate-400 font-mono">({p.event_type.replace('_', ' ')})</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-cyan-400 px-2 py-0.5 bg-cyan-500/10 rounded">{p.prediction_strength}</span>
                    <span className="text-slate-400 text-xs">{isOpen ? '▲' : '▼'}</span>
                  </div>
                </button>

                {isOpen && (
                  <div className="p-4 border-t border-slate-800 space-y-3 text-xs text-slate-300 font-sans">
                    <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 text-slate-200 leading-relaxed">
                      {p.summary}
                    </div>

                    {p.supporting_factors && p.supporting_factors.length > 0 && (
                      <div>
                        <span className="font-bold text-amber-400 block mb-1">Key Causal Drivers:</span>
                        <ul className="list-disc list-inside space-y-1 text-slate-300">
                          {p.supporting_factors.map((factor, fIdx) => (
                            <li key={fIdx}>{factor}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {p.practical_actions && p.practical_actions.length > 0 && (
                      <div>
                        <span className="font-bold text-cyan-400 block mb-1">Strategic Action Protocol:</span>
                        <ul className="list-disc list-inside space-y-1 text-slate-300">
                          {p.practical_actions.map((act, aIdx) => (
                            <li key={aIdx}>{act}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ) : reportMarkdown ? (
        <div className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed whitespace-pre-line font-sans p-4 bg-slate-800/20 rounded-xl border border-slate-800">
          {reportMarkdown}
        </div>
      ) : (
        <div className="text-center py-8 text-slate-400 text-xs font-mono">
          Select or load a birth profile report to view confluent predictions.
        </div>
      )}
    </div>
  );
};
