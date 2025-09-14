import "./index.css";
import { useState } from "react";

export default function App() {
  const [mode, setMode] = useState("text"); // "text" or "image"
  const [text, setText] = useState("");
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (mode === "text" && text.trim()) {
      setResult("✅ Analysis complete: No misinformation detected.");
    } else if (mode === "image" && image) {
      setResult("⚠️ Image may contain misleading information.");
    } else {
      setResult("Please provide valid input.");
    }
  };

  return (
    <div className="min-h-screen relative flex flex-col items-center p-6 overflow-hidden">
      <div className="absolute inset-0 -z-10">
        <div className="w-full h-full bg-gradient-to-br from-[#a7bfff] via-[#f8fafc] to-[#c7d2fe] opacity-95 animate-gradient-x" />
        <svg
          className="absolute top-0 left-0 w-full h-full opacity-25"
          width="100%"
          height="100%"
          viewBox="0 0 1440 900"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="none"
        >
          <defs>
            <pattern
              id="grid"
              width="60"
              height="60"
              patternUnits="userSpaceOnUse"
            >
              <path
                d="M 60 0 L 0 0 0 60"
                fill="none"
                stroke="#818cf8"
                strokeWidth="0.7"
              />
            </pattern>
            <radialGradient id="radial" cx="50%" cy="50%" r="80%">
              <stop offset="0%" stopColor="#a5b4fc" stopOpacity="0.2" />
              <stop offset="100%" stopColor="#818cf8" stopOpacity="0" />
            </radialGradient>
          </defs>
          <rect width="1440" height="900" fill="url(#grid)" />
          <circle
            cx="1200"
            cy="200"
            r="140"
            fill="url(#radial)"
            fillOpacity="0.25"
          />
          <circle cx="300" cy="700" r="200" fill="#6366f1" fillOpacity="0.12" />
          <ellipse
            cx="900"
            cy="600"
            rx="120"
            ry="60"
            fill="#818cf8"
            fillOpacity="0.10"
          />
        </svg>
        <div className="absolute top-[-100px] left-[-100px] w-[300px] h-[300px] bg-indigo-200 rounded-full blur-3xl opacity-40 animate-blob" />
        <div className="absolute bottom-[-120px] right-[-120px] w-[320px] h-[320px] bg-blue-200 rounded-full blur-3xl opacity-40 animate-blob animation-delay-2000" />
      </div>

      <header className="text-center mb-12 mt-10">
        <h1 className="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-700 via-blue-600 to-purple-600 drop-shadow-lg mb-4 tracking-tight">
          AI-powered Misinformation Detector
        </h1>
        <p className="text-[#475569] text-lg md:text-xl max-w-2xl mx-auto font-medium drop-shadow-sm">
          Analyze news articles, social media posts, and images for potential
          misinformation using advanced AI. Get instant credibility scores,
          fact-checking insights, and source verification to help you make
          informed decisions.
        </p>
      </header>

      {/* Features Section */}
      <section className="flex flex-col md:flex-row gap-8 mb-14 w-full max-w-3xl justify-center">
        {/* Text Analysis */}
        <div className="flex-1 bg-white/90 rounded-2xl border border-slate-200 shadow-xl hover:shadow-2xl transition-all p-7 flex flex-col items-start backdrop-blur-lg hover:scale-105 duration-200">
          <div className="bg-gradient-to-tr from-green-200 to-green-100 rounded-full p-3 mb-5 shadow">
            <svg
              className="w-8 h-8 text-green-500"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h3 className="font-bold text-xl text-[#334155] mb-2">
            Text Analysis
          </h3>
          <p className="text-[#64748b] text-base">
            Analyze written content for misleading claims, biased language, and
            factual inconsistencies.
          </p>
        </div>
        {/* Image Analysis */}
        <div className="flex-1 bg-white/90 rounded-2xl border border-slate-200 shadow-xl hover:shadow-2xl transition-all p-7 flex flex-col items-start backdrop-blur-lg hover:scale-105 duration-200">
          <div className="bg-gradient-to-tr from-purple-200 to-purple-100 rounded-full p-3 mb-5 shadow">
            <svg
              className="w-8 h-8 text-purple-500"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <rect width="20" height="14" x="2" y="5" rx="2" />
              <circle cx="8.5" cy="10.5" r="1.5" />
              <path d="M21 19l-5.5-5.5a2.121 2.121 0 00-3 0L3 19" />
            </svg>
          </div>
          <h3 className="font-bold text-xl text-[#334155] mb-2">
            Image Analysis
          </h3>
          <p className="text-[#64748b] text-base">
            Detect manipulated images, deepfakes, and verify the authenticity of
            visual content.
          </p>
        </div>
      </section>

      {/* Mode Switch */}
      <div className="flex space-x-4 mb-7">
        <button
          onClick={() => setMode("text")}
          className={`px-7 py-2.5 rounded-full font-semibold shadow transition-all duration-200 border-2 text-lg ${
            mode === "text"
              ? "bg-gradient-to-r from-blue-500 to-indigo-500 text-white border-blue-400 ring-2 ring-blue-200 scale-105"
              : "bg-white text-[#334155] border-slate-200 hover:bg-blue-50"
          }`}
        >
          Text / Article
        </button>
        <button
          onClick={() => setMode("image")}
          className={`px-7 py-2.5 rounded-full font-semibold shadow transition-all duration-200 border-2 text-lg ${
            mode === "image"
              ? "bg-gradient-to-r from-purple-500 to-indigo-500 text-white border-purple-400 ring-2 ring-purple-200 scale-105"
              : "bg-white text-[#334155] border-slate-200 hover:bg-purple-50"
          }`}
        >
          Image
        </button>
      </div>

      {/* Input Form */}
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-lg bg-white/80 backdrop-blur-lg p-10 rounded-3xl shadow-2xl border border-slate-100"
      >
        {mode === "text" ? (
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste news article or text here..."
            className="w-full p-4 border border-slate-200 rounded-xl mb-6 focus:ring-2 focus:ring-blue-300 outline-none bg-blue-50/40 text-[#334155] text-lg transition"
            rows="6"
          />
        ) : (
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files[0])}
            className="w-full p-3 border border-slate-200 rounded-xl mb-6 focus:ring-2 focus:ring-purple-300 outline-none bg-purple-50/40 text-[#334155] text-lg transition"
          />
        )}

        <button
          type="submit"
          className="w-full bg-gradient-to-r from-indigo-500 to-blue-500 text-white py-3 rounded-xl font-bold text-lg hover:from-indigo-600 hover:to-blue-600 transition shadow-lg"
        >
          Analyze
        </button>
      </form>

      {/* Result Box */}
      {result && (
        <div className="mt-10 w-full max-w-lg bg-gradient-to-r from-blue-100/80 via-white/90 to-indigo-100/80 p-6 rounded-2xl text-[#334155] border border-blue-100 shadow-xl font-semibold text-xl backdrop-blur-lg">
          <strong className="block mb-1 text-blue-700">Result:</strong> {result}
        </div>
      )}

      {/* Custom Animations */}
      <style>
        {`
          .animate-gradient-x {
            background-size: 200% 200%;
            animation: gradient-x 8s ease-in-out infinite;
          }
          @keyframes gradient-x {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
          }
          .animate-blob {
            animation: blob 12s infinite;
          }
          .animation-delay-2000 {
            animation-delay: 2s;
          }
          @keyframes blob {
            0%, 100% { transform: translateY(0px) scale(1); }
            33% { transform: translateY(30px) scale(1.1); }
            66% { transform: translateY(-20px) scale(0.95); }
          }
        `}
      </style>
    </div>
  );
}
