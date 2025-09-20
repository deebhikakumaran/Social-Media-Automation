import { useState } from "react";
import { Link } from "react-router-dom";
import "../styles/Post.css";

const Header = () => {
  return (
    <header className="navbar">
      <div className="logo">Strydo</div>
      <ul className="navbar-links"> 
        <Link to="/link">Link to Content</Link>
        <Link to="/post">Text to Content</Link>
      </ul>
      <Link to="/" className="btn btn-primary">
        Go Back
      </Link>
    </header>
  );
};

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <p>© 2025 Strydo All rights reserved.</p>
      </div>
    </footer>
  );
};

const Post = () => {
  const [scriptContext, setScriptContext] = useState("");
  const [generatedContent, setGeneratedContent] = useState(null);
  const [postStatus, setPostStatus] = useState("");
  const [postLink, setPostLink] = useState("");
  const [conversationId, setConversationId] = useState(null);

  const handleGenerate = async () => {
    setGeneratedContent(null);
    setPostStatus("Generating...");
    setPostLink("");

    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_context: scriptContext }),
      });

      const data = await response.json();
      if (response.ok) {
        setPostStatus(data.status);
        setGeneratedContent(data.result);
        setConversationId(data.conversation_id);
      } else {
        setPostStatus(data.detail || "Failed to generate script.");
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      setPostStatus("Failed to submit.");
    }
  };

  const handleApprove = async () => {
    setPostStatus("Posting to LinkedIn...");
    setPostLink("");

    try {
      const response = await fetch("http://localhost:8000/post", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          final_script: generatedContent, 
          user_approval: true,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setPostStatus(data.status);
        if (data.status.includes("successful")) {
          setPostLink("https://www.linkedin.com/feed"); 
        }
      } else {
        setPostStatus(data.detail || "Failed to post script.");
      }
    } catch (error) {
      console.error("Error posting to LinkedIn:", error);
      setPostStatus("Failed to post.");
    }
  };

  return (
    <>
      <meta charSet="utf-8" />
      <link
        rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
      />

      <style
        dangerouslySetInnerHTML={{
          __html: `
            :root {
                --dark-gray: #1E1F27;
                --orange-gradient-top: #E58D45;
                --orange-gradient-bottom: #C45D1C;
                --button-orange: #C45D1C;
                --light-gray-bg: #EAEBF2;
                --quote-bg: #F0F0F0;
                --text-dark: #333;
                --text-light: #f5f5f5;
                --nav-links: #666;
                --nav-button-text: #fff;
                --footer-text: #A0A0A0;
                --border-orange: #C45D1C;
                --primary-light: #b9c3d3;
            }
            body {
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 0;
                background-color: var(--dark-gray);
                color: var(--text-dark);
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }
            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 20px 40px;
                background-color: transparent;
            }
            .navbar .logo {
                font-weight: 700;
                font-size: 1.5em;
                color: var(--button-orange);
            }
            .navbar-links {
                list-style: none;
                display: flex;
                gap: 25px;
                font-weight: 500;
            }
            .navbar-links a {
                text-decoration: none;
                color: var(--nav-links);
            }
            .btn {
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: 600;
                text-decoration: none;
                transition: background-color 0.3s;
            }
            .btn-primary {
                background-color: var(--button-orange);
                color: var(--nav-button-text);
            }
            .btn-primary:hover {
                background-color: #A04A15;
            }
            .post-page{
                background: linear-gradient(180deg, var(--orange-gradient-top), var(--orange-gradient-bottom));
            }
            .chat-container {
                margin: 0 auto;
                padding: 2rem 20px;
                display: flex;
                gap: 2rem;
                height: 100vh;
            }
            .chat-box {
                flex: 1;
                background-color: #fff;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border: 1px solid var(--primary-color);
            }
            .preview-box {
                flex: 1;
                background-color: var(--quote-bg);
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                border: 1px solid var(--primary-color);
            }
            .post-actions {
                display: flex;
                gap: 1rem;
                margin-top: 1rem;
            }
            .status-message {
                margin-top: 1rem;
                font-size: 1.1em;
                font-weight: 500;
            }
            .status-link {
                color: var(--button-orange);
                text-decoration: none;
                font-weight: 600;
            }
            .footer {
                background-color: var(--dark-gray);
                color: var(--footer-text);
                text-align: center;
                padding: 10px;
                font-size: 0.9em;
            }
          `,
        }}
      />

      <div className="layout-container flex h-full grow flex-col">
        <Header />
        <main className="flex-1 post-page">
          <div className="chat-container">
            <div className="chat-box">
              <h2 style={{ color: "var(--primary-color)" }}>
                Script Generation Agent
              </h2>
              <textarea
                className="w-full h-48 p-2 mt-4 border border-gray-400 rounded"
                rows="20"
                cols="60"
                placeholder="Enter script context here..."
                value={scriptContext}
                onChange={(e) => setScriptContext(e.target.value)}
              ></textarea>
              <div className="post-actions mt-auto">
                <button
                  onClick={handleGenerate}
                  className="btn btn-primary"
                  disabled={!scriptContext}
                >
                  Generate Content
                </button>
              </div>
            </div>
            <div className="preview-box">
              <h2 style={{ color: "var(--primary-color)" }}>
                Generated Preview
              </h2>

              <div
                className="preview-content"
                style={{
                  height: "300px",
                  overflowY: "auto",
                  border: "1px solid #171717ff",
                  padding: "10px",
                  borderRadius: "4px",
                  backgroundColor: "#fff",
                }}
              >
                <p
                  className="whitespace-pre-wrap mt-4"
                  style={{ color: "var(--text-dark)" }}
                >
                  {generatedContent ||
                    "Your generated content will appear here..."}
                </p>
              </div>

              <div className="post-actions mt-auto">
                <button
                  onClick={handleApprove}
                  className="btn btn-primary"
                  disabled={!generatedContent}
                >
                  Approve & Post
                </button>
              </div>
              {postStatus && (
                <div className="status-message">
                  {postStatus}
                  {postLink && (
                    <a href={postLink} target="_blank" className="status-link">
                      {" "}
                      View post
                    </a>
                  )}
                </div>
              )}
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </>
  );
};

export default Post;
