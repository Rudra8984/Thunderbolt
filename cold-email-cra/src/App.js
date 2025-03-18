import React, { useState } from "react";
import { Upload, Search, Mail, Edit3, Send, Loader2 } from "lucide-react";
import axios from "axios";
import "./temp.css";

function App() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [file, setFile] = useState(null);
  const [researcher, setResearcher] = useState("");
  const [researcherData, setResearcherData] = useState(null);
  const [emailTemplates, setEmailTemplates] = useState([]);

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setLoading(true);
    setFile(selectedFile);

    const formData = new FormData();
    formData.append("resume", selectedFile);

    try {
      await axios.post("http://localhost:8000/api/upload-resume/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setStep(2);
    } catch (error) {
      console.error("Error uploading resume:", error);
      alert("Failed to upload resume.");
    } finally {
      setLoading(false);
    }
  };

  const handleResearcherSearch = async (e) => {
    e.preventDefault();
    if (!researcher.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/search-researcher/",
        {
          researcher: researcher,
        }
      );

      if (response.data.error) {
        alert(response.data.error);
        setResearcherData(null);
      } else {
        setResearcherData(response.data); // ✅ Fixed: Data loads correctly
        setStep(3);
      }
    } catch (error) {
      console.error("Error searching researcher:", error);
      alert("Error fetching researcher data.");
    } finally {
      setLoading(false);
    }
  };

  const handleFetchEmails = async () => {
    if (!researcherData) return;

    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/get-email-templates/",
        {
          researcher: researcherData.researcher, // ✅ Send researcher name
          title: researcherData.papers[0]?.title || "No Title",
          abstract: researcherData.papers[0]?.abstract || "No Abstract",
          skills: "Extracted Skills Here", // You may replace this with actual extracted skills
          projects: "Extracted Projects Here",
        }
      );

      setEmailTemplates(response.data);
      setStep(4);
    } catch (error) {
      console.error("Error fetching email templates:", error);
      alert("Failed to fetch email templates.");
    } finally {
      setLoading(false);
    }
  };

  const handleSendEmail = async () => {
    if (!selectedTemplate) return;

    setLoading(true);
    try {
      await axios.post("http://localhost:8000/api/send-email/", {
        template: selectedTemplate,
        researcher: researcherData.researcher,
        resumeId: file?.name || "test_resume.pdf",
      });
      alert("Email sent successfully!");
    } catch (error) {
      console.error("Error sending email:", error);
      alert("Failed to send email. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="nav-content">
          <div className="logo">
            <Mail className="icon" />
            <span className="title">ResearchReach</span>
          </div>
          <div className="status-indicator">
            <div className="status-dot"></div>
            <span className="status-text">APIs Connected</span>
          </div>
        </div>
      </nav>

      <main className="main-content">
        <div className="header-section">
          <h1 className="main-title">Research Internship Email Generator</h1>
          <div className="step-indicator">
            <span>Step {step}</span>
            <span>/</span>
            <span>4</span>
          </div>
        </div>

        <div className="card">
          {/* Step 1: Resume Upload */}
          <div className={`step-container ${step !== 1 ? "hidden" : ""}`}>
            <div className="step">
              <Upload className="step-icon" />
              <h2>Upload Your Resume</h2>
              <p>
                We'll analyze your experience to find relevant research matches
              </p>
              <label className="file-upload-label">
                <input
                  type="file"
                  className="file-input"
                  accept=".pdf,.doc,.docx"
                  onChange={handleFileUpload}
                />
                <div className="upload-area">
                  <Upload className="upload-icon" />
                  <span>Upload Resume (PDF, DOC, DOCX)</span>
                </div>
              </label>
            </div>
          </div>

          {/* Step 2: Researcher Search */}
          <div className={`step-container ${step !== 2 ? "hidden" : ""}`}>
            <div className="step">
              <Search className="step-icon" />
              <h2>Find a Researcher</h2>
              <p>Search for the researcher you'd like to contact</p>
              <form onSubmit={handleResearcherSearch} className="search-form">
                <div className="search-group">
                  <input
                    type="text"
                    value={researcher}
                    onChange={(e) => setResearcher(e.target.value)}
                    placeholder="Enter researcher name or institution"
                    className="search-input"
                  />
                  <button type="submit" className="btn">
                    Search
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Step 3: Display Research Papers */}
          <div className={`step-container ${step !== 3 ? "hidden" : ""}`}>
            <div className="step">
              <Edit3 className="step-icon" />
              <h2>Matching Research Papers</h2>
              <p>These papers match your profile</p>

              {loading ? (
                <p>
                  <Loader2 className="loading-icon" /> Loading papers...
                </p>
              ) : researcherData ? (
                <div className="research-list">
                  <h3>{researcherData.researcher}</h3>
                  <ul>
                    {researcherData.papers.map((paper, index) => (
                      <li key={index} className="paper-item">
                        <strong>{paper.title}</strong>
                        <p>{paper.abstract || "No abstract available."}</p>
                        <a
                          href={paper.link}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          View Paper
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : (
                <p>No research papers found.</p>
              )}

              <button onClick={handleFetchEmails} className="btn">
                Proceed to Email Templates
              </button>
            </div>
          </div>

          {/* Step 4: Email Templates */}
          <div className={selectedTemplate ? "Fixer" : ""}>
            <div className={`step-container ${step !== 4 ? "hidden" : ""}`}>
              <div className={`${selectedTemplate ? "step-4" : "step"}`}>
                <Edit3 className="step-icon" />
                <h2>Choose Your Email Template</h2>
                <p>Select and customize your preferred email style</p>

                <div className="templates-grid">
                  {emailTemplates.map((template, index) => (
                    <div
                      key={index}
                      className={`template-card ${
                        selectedTemplate?.type === template.type
                          ? "selected"
                          : ""
                      }`}
                      onClick={() => setSelectedTemplate(template)}
                    >
                      <h3>{template.type}</h3>
                      <p>{template.content.substring(0, 100)}...</p>
                    </div>
                  ))}
                </div>

                <button onClick={handleSendEmail} className="btn send-button">
                  <Send className="btn-icon" />
                  Send Email
                </button>
              </div>
              {selectedTemplate && (
                <div className="email-editor">
                  <textarea
                    className="email-content"
                    value={selectedTemplate.content}
                    onChange={(e) =>
                      setSelectedTemplate({
                        ...selectedTemplate,
                        content: e.target.value,
                      })
                    }
                  />
                  <button onClick={handleSendEmail} className="btn send-button">
                    <Send className="btn-icon" />
                    Send Email
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
