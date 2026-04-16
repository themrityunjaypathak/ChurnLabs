import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL as string;


type FormDataType = {
  [key: string]: string;
};


type PredictionResponse = {
  churn_probability: number;
  prediction: number;
  threshold_used: number;
};


type SelectFieldProps = {
  label: string;
  name: string;
  options: string[];
  formData: FormDataType;
  handleChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
};


const SelectField = ({
  label,
  name,
  options,
  formData,
  handleChange,
}: SelectFieldProps) => (
  <div className="form-group">
    <label>{label}</label>
    <select name={name} value={formData[name]} onChange={handleChange}>
      {options.map((opt) => (
        <option key={opt} value={opt}>
          {opt}
        </option>
      ))}
    </select>
  </div>
);


type NumberFieldProps = {
  label: string;
  name: string;
  formData: FormDataType;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
};


const NumberField = ({
  label,
  name,
  formData,
  handleChange,
}: NumberFieldProps) => (
  <div className="form-group">
    <label>{label}</label>
    <input
      type="number"
      step="any"
      name={name}
      value={formData[name]}
      onChange={handleChange}
      required
    />
  </div>
);


function App() {
  const [menuOpen, setMenuOpen] = useState<boolean>(false);
  const [formOpen, setFormOpen] = useState<boolean>(
    window.innerWidth <= 768
  );

  const [formData, setFormData] = useState<FormDataType>({
    gender: "Male",
    seniorcitizen: "0",
    partner: "Yes",
    dependents: "No",
    tenure: "12",
    phoneservice: "Yes",
    multiplelines: "No",
    internetservice: "DSL",
    onlinesecurity: "No",
    onlinebackup: "Yes",
    deviceprotection: "No",
    techsupport: "No",
    streamingtv: "Yes",
    streamingmovies: "No",
    contract: "Month-to-month",
    paperlessbilling: "Yes",
    paymentmethod: "Electronic check",
    monthlycharges: "40.35",
    totalcharges: "165.35",
  });

  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const payload = {
        ...formData,
        seniorcitizen: formData.seniorcitizen === "Yes" ? 1 : 0,
        tenure: Number(formData.tenure),
        monthlycharges: Number(formData.monthlycharges),
        totalcharges: Number(formData.totalcharges),
      };

      const response = await axios.post<PredictionResponse>(
        `${API_URL}/predict`,
        payload
      );

      setTimeout(() => {
        setResult(response.data);
        setLoading(false);
      }, 800);
    } catch (err) {
      setError("Prediction failed. Please check backend.");
      setLoading(false);
    }
  };

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth <= 768) {
        setFormOpen(true);
      } else {
        setFormOpen(false);
      }
    };

    handleResize();
    window.addEventListener("resize", handleResize);

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="app">

      {/* NAVBAR */}

      <header className="navbar">

        <div className="logo">
          <img src="logo.png" alt="ChurnLabs Logo" /><p>ChurnLabs</p>
        </div>

        <nav className="nav-links">

          <a
            href="https://github.com/themrityunjaypathak/ChurnLabs"
            target="_blank"
            rel="noreferrer"
          >
            GitHub
          </a>

          <a
            href="https://churnlabs.onrender.com/docs"
            target="_blank"
            rel="noreferrer"
          >
            API Docs
          </a>

          <a
            href="https://hub.docker.com/r/themrityunjaypathak"
            target="_blank"
            rel="noreferrer"
          >
            Docker Hub
          </a>

        </nav>

        <div className="star">
          <a
            href="https://github.com/themrityunjaypathak/ChurnLabs"
            target="_blank"
            rel="noreferrer"
          >
            <i className="fa-solid fa-star"></i>Star on GitHub
          </a>
        </div>

        <div
          className="hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <i className={menuOpen ? "fa-solid fa-xmark" : "fa-solid fa-bars"}></i>
        </div>

      </header>

      {/* MOBILE MENU */}

      <div className={`mobile-menu ${menuOpen ? "active" : ""}`}>

        <a
          href="https://github.com/themrityunjaypathak/ChurnLabs"
          target="_blank"
          rel="noreferrer"
        >
          GitHub
        </a>

        <a
          href="https://churnlabs.onrender.com/docs"
          target="_blank"
          rel="noreferrer"
        >
          API Docs
        </a>

        <a
          href="https://hub.docker.com/r/themrityunjaypathak"
          target="_blank"
          rel="noreferrer"
        >
          Docker Hub
        </a>

        <a
          href="https://github.com/themrityunjaypathak/ChurnLabs"
          target="_blank"
          rel="noreferrer"
          className="star-btn"
        >
          <i className="fa-solid fa-star"></i> Star on GitHub
        </a>

      </div>

      <div className="hero-image">
        <img src="hero-image.png" alt="Customer Churn Illustration" />
      </div>

      {/* CARD */}

      <div className="card">

        <div
          className="form-expander-header"
          onClick={() => setFormOpen(!formOpen)}
        >

          <h3>Fill in the Customer Details</h3>

          <span className={`arrow ${formOpen ? "open" : ""}`}>
            <i className="fa-solid fa-chevron-down"></i>
          </span>

        </div>

        <div className={`form-expander ${formOpen ? "open" : ""}`}>

          <form onSubmit={handleSubmit} className="form">

            <SelectField label="Gender" name="gender" options={["Male", "Female"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Senior Citizen" name="seniorcitizen" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Partner" name="partner" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Dependents" name="dependents" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <NumberField label="Tenure (Months)" name="tenure" formData={formData} handleChange={handleChange} />
            <SelectField label="Phone Service" name="phoneservice" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Multiple Lines" name="multiplelines" options={["Yes", "No", "No phone service"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Internet Service" name="internetservice" options={["DSL", "Fiber optic", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Online Security" name="onlinesecurity" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Online Backup" name="onlinebackup" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Device Protection" name="deviceprotection" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Tech Support" name="techsupport" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Streaming TV" name="streamingtv" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />
            <SelectField label="Streaming Movies" name="streamingmovies" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />

            <div className="full-width">
              <SelectField label="Contract" name="contract" options={["Month-to-month", "One year", "Two year"]} formData={formData} handleChange={handleChange} />
            </div>

            <SelectField label="Paperless Billing" name="paperlessbilling" options={["Yes", "No"]} formData={formData} handleChange={handleChange} />

            <SelectField
              label="Payment Method"
              name="paymentmethod"
              options={[
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
              ]}
              formData={formData}
              handleChange={handleChange}
            />

            <NumberField label="Monthly Charges" name="monthlycharges" formData={formData} handleChange={handleChange} />
            <NumberField label="Total Charges" name="totalcharges" formData={formData} handleChange={handleChange} />

            <button type="submit">
              <i className="fa-solid fa-bolt"></i> {loading ? "Analyzing..." : "Run Prediction"}
            </button>

          </form>

        </div>

        {error && <div className="error">{error}</div>}

        {result && (
          <div className={`result ${result.prediction === 1 ? "danger" : "success"}`}>
            <h2>{result.prediction === 1 ? "🔴 High Churn Risk" : "🟢 Low Churn Risk"}</h2>

            <div className="bar">
              <div
                className="fill"
                style={{ width: `${result.churn_probability * 100}%` }}
              />
            </div>

            <p>{(result.churn_probability * 100).toFixed(0)}% Probability</p>
          </div>
        )}

      </div>

    </div>
  );
}

export default App;