import React, { useState } from 'react';

export interface ReportViewerProps {
  reportMarkdown: string;
  onLanguageChange?: (langCode: string) => void;
}

export const ReportViewer: React.FC<ReportViewerProps> = ({
  reportMarkdown,
  onLanguageChange
}) => {
  const [selectedLang, setSelectedLang] = useState<string>('en');

  const handleLangSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const code = e.target.value;
    setSelectedLang(code);
    if (onLanguageChange) {
      onLanguageChange(code);
    }
  };

  return (
    <div className="card-glass p-6 rounded-2xl border border-white/10 text-white space-y-4">
      <div className="flex justify-between items-center border-b border-white/10 pb-4">
        <h2 className="text-2xl font-bold font-serif text-amber-400">Astrological Intelligence Report</h2>
        <div className="flex items-center gap-2">
          <label htmlFor="lang-select" className="text-xs text-slate-300 font-mono">Language / ഭാഷ / भाषा:</label>
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

      <div className="prose prose-invert max-w-none text-slate-200 text-sm leading-relaxed whitespace-pre-line font-sans">
        {reportMarkdown}
      </div>
    </div>
  );
};
