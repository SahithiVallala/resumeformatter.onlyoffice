import React, { useState, useEffect } from 'react';
import WizardStepper from './components/WizardStepper';
import TemplateSelection from './components/TemplateSelection';
import ResumeUploadPhase from './components/ResumeUploadPhase';
import DownloadPhase from './components/DownloadPhase';
import './App.css';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [results, setResults] = useState([]);
  const [isFormatting, setIsFormatting] = useState(false);

  const fetchTemplates = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/templates');
      const data = await response.json();
      if (data.success) {
        setTemplates(data.templates);
      }
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  useEffect(() => {
    fetchTemplates();
  }, []);

  const handleTemplateDelete = async (templateId) => {
    if (window.confirm('Are you sure you want to delete this template?')) {
      try {
        await fetch(`http://localhost:5000/api/templates/${templateId}`, {
          method: 'DELETE'
        });
        fetchTemplates();
        if (selectedTemplate === templateId) {
          setSelectedTemplate(null);
        }
      } catch (error) {
        alert('Error deleting template');
      }
    }
  };

  const handleTemplateSelect = (templateId) => {
    setSelectedTemplate(templateId);
    // Auto-advance to next step after selection
    setTimeout(() => setCurrentStep(2), 500);
  };

  const handleTemplateUpload = () => {
    fetchTemplates();
  };

  const handleFormatSuccess = (formattedResults) => {
    setResults(formattedResults);
    setIsFormatting(false);
    setCurrentStep(3);
  };

  const handleStartOver = () => {
    setCurrentStep(1);
    setSelectedTemplate(null);
    setResults([]);
  };

  const steps = [
    { number: 1, title: 'Select Template', icon: '📋' },
    { number: 2, title: 'Upload Resumes', icon: '📄' },
    { number: 3, title: 'Download Results', icon: '📥' }
  ];

  return (
    <div className="App">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">✨</span>
            <h1>Resume Formatter Pro</h1>
          </div>
          <p className="tagline">Transform Your Resumes with Professional Templates</p>
        </div>
      </header>

      <div className="main-container">
        <WizardStepper steps={steps} currentStep={currentStep} />

        <div className="wizard-content">
          {currentStep === 1 && (
            <TemplateSelection
              templates={templates}
              selectedTemplate={selectedTemplate}
              onSelect={handleTemplateSelect}
              onDelete={handleTemplateDelete}
              onUpload={handleTemplateUpload}
            />
          )}

          {currentStep === 2 && (
            <ResumeUploadPhase
              selectedTemplate={selectedTemplate}
              templates={templates}
              onFormatSuccess={handleFormatSuccess}
              onBack={() => setCurrentStep(1)}
              isFormatting={isFormatting}
              setIsFormatting={setIsFormatting}
            />
          )}

          {currentStep === 3 && (
            <DownloadPhase
              results={results}
              onStartOver={handleStartOver}
            />
          )}
        </div>
      </div>

      <footer className="footer">
        <p>© 2025 Resume Formatter Pro • Powered by AI</p>
      </footer>
    </div>
  );
}

export default App;
