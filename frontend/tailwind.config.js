/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Plus Jakarta Sans", "ui-sans-serif", "system-ui"],
      },
      colors: {
        night: {
          900: "#0b1120",
          800: "#111827",
          700: "#1f2937",
        },
        aurora: {
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
        },
      },
      boxShadow: {
        glow: "0 10px 40px rgba(37, 99, 235, 0.25)",
        glass: "0 20px 50px rgba(15, 23, 42, 0.2)",
      },
      backgroundImage: {
        grid: "radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.25) 0%, transparent 50%), radial-gradient(circle at 80% 0%, rgba(14, 165, 233, 0.18) 0%, transparent 55%), radial-gradient(circle at 30% 80%, rgba(99, 102, 241, 0.2) 0%, transparent 50%)",
      },
    },
  },
  plugins: [],
};
