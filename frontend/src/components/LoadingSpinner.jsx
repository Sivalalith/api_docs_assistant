function LoadingSpinner({ text = "Loading..." }) {
  return (
    <div className="flex items-center justify-center gap-2">
      <div
        className="
          w-5
          h-5
          border-2
          border-blue-600
          border-t-transparent
          rounded-full
          animate-spin
        "
      ></div>

      <span className="text-slate-600 font-medium">{text}</span>
    </div>
  );
}

export default LoadingSpinner;
