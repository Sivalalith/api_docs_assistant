import { useEffect, useState } from "react";
import { checkBackendHealth } from "./services/healthService";

function App() {
  const [status, setStatus] = useState("Connecting...");

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const data = await checkBackendHealth();
        setStatus(data.status);
      } catch (error) {
        setStatus("Backend connection failed!");
        console.error(error);
      }
    };

    fetchHealth();
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <h1 className="text-3xl font-bold">{status}</h1>
    </div>
  );
}

export default App;
