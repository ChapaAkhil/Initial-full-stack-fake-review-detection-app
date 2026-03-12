const features = [
  "Fake Review Detection",
  "Behavioral Feature Analysis",
  "Review Authenticity Percentage",
  "Machine Learning Prediction",
  "Manual Review Testing",
];

export default function Overview() {
  return (
    <section className="mt-10 grid gap-6 lg:grid-cols-[1.2fr_1fr]">
      <div className="glass-card p-6">
        <p className="section-subtitle">Project Overview</p>
        <h2 className="section-title mt-3">Intelligent review authenticity analysis.</h2>
        <p className="mt-3 text-sm leading-relaxed text-white/70">
          This system uses machine learning techniques to analyze product reviews and classify them as
          genuine or fake. It evaluates review text and behavioral features such as rating consistency,
          helpful votes, review timing, and reviewer activity patterns.
        </p>
      </div>
      <div className="grid gap-4">
        {features.map((feature) => (
          <div key={feature} className="glass-card px-4 py-4 text-sm text-white/80">
            {feature}
          </div>
        ))}
      </div>
    </section>
  );
}
