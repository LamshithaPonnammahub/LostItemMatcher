import React from 'react';

// Simple, dependency-free SVG line chart for accuracy over epochs.
// Props:
// - data: array of numbers (accuracy values between 0 and 1 or 0-100)
// - labels: array of labels (optional)
// Renders a responsive SVG with axes, gridlines, and a smooth line.
export default function AccuracyChart({ data = [0.5, 0.62, 0.7, 0.78, 0.83, 0.86, 0.9], labels }) {
  // Normalize data to 0..1 (if values are between 0 and 100)
  const normalized = data.map((v) => (v > 1 ? v / 100 : v));

  const width = 700;
  const height = 300;
  const padding = { top: 20, right: 20, bottom: 40, left: 50 };

  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;

  const max = Math.max(...normalized, 1);
  const min = Math.min(...normalized, 0);

  const points = normalized.map((val, i) => {
    const x = padding.left + (i / Math.max(1, normalized.length - 1)) * innerWidth;
    const y = padding.top + (1 - (val - min) / (max - min || 1)) * innerHeight;
    return { x, y, val };
  });

  const pathD = points
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x.toFixed(2)} ${p.y.toFixed(2)}`)
    .join(' ');

  const yTicks = 5;
  const yLabels = Array.from({ length: yTicks + 1 }, (_, i) => {
    const t = i / yTicks;
    const value = (min + (1 - t) * (max - min));
    return { t, value };
  });

  return (
    <div className="chart-card">
      <h2>Model Accuracy</h2>
      <svg viewBox={`0 0 ${width} ${height}`} width="100%" height="auto" preserveAspectRatio="xMidYMid meet">
        {/* Y grid and labels */}
        {yLabels.map((lbl, idx) => {
          const y = padding.top + lbl.t * innerHeight;
          return (
            <g key={idx}>
              <line x1={padding.left} x2={width - padding.right} y1={y} y2={y} stroke="#eee" />
              <text x={padding.left - 10} y={y + 4} fontSize="12" textAnchor="end" fill="#666">
                {(lbl.value * 100).toFixed(0)}%
              </text>
            </g>
          );
        })}

        {/* X labels */}
        {points.map((p, i) => (
          <text key={i} x={p.x} y={height - 8} fontSize="11" textAnchor="middle" fill="#666">
            {labels?.[i] ?? `E${i + 1}`}
          </text>
        ))}

        {/* Line path */}
        <path d={pathD} fill="none" stroke="#4caf50" strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" />

        {/* Area under curve (light) */}
        <path
          d={`${pathD} L ${padding.left + innerWidth} ${padding.top + innerHeight} L ${padding.left} ${padding.top + innerHeight} Z`}
          fill="#4caf5077"
        />

        {/* Points */}
        {points.map((p, i) => (
          <g key={i}>
            <circle cx={p.x} cy={p.y} r={4.5} fill="#fff" stroke="#388e3c" strokeWidth={2} />
            <title>{`${labels?.[i] ?? `Epoch ${i + 1}`}: ${(p.val * 100).toFixed(1)}%`}</title>
          </g>
        ))}
      </svg>
      <p className="chart-note">This chart shows model accuracy across training epochs (sample/demo data).</p>
    </div>
  );
}
