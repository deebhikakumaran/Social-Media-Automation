import { useState } from 'react';
import { Link } from 'react-router-dom';

const LinkToContent = () => {
    const [url, setUrl] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!url) {
            setMessage('Please enter a valid URL.');
            return;
        }

        setIsLoading(true);
        setMessage('');

        try {
            const response = await fetch('http://127.0.0.1:8000/run-agent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            if (response.ok) {
                const data = await response.json();
                setMessage(data.message || 'Content posted successfully!');
            } else {
                const errorData = await response.json();
                setMessage(errorData.detail || 'Failed to post content. Please try again.');
            }
        } catch (error) {
            setMessage('An error occurred. Please check your network and try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
      <meta charSet="utf-8" />
      <link
        rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
      />
        <div className="layout-container" style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', backgroundColor: '#F8E7D8' }}>
            <style dangerouslySetInnerHTML={{
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
                    }
                    body {
                        font-family: 'Poppins', sans-serif;
                        margin: 0;
                        padding: 0;
                        background-color: var(--dark-gray);
                        color: var(--text-dark);
                    }
                    .navbar {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 20px 40px;
                        background-color: var(--dark-gray);
                        width: 100%;
                        position: absolute;
                        top: 0;
                        left: 0;
                        box-sizing: border-box;
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
                    .main-content {
                        flex-grow: 1; /* Pushes footer down */
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                        padding: 20px;
                    }
                    .content-form {
                        background: #F0F0F0;
                        padding: 40px;
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                        max-width: 500px;
                        width: 100%;
                    }
                    .content-form h1 {
                        color: #555;
                        font-size: 2em;
                        margin-bottom: 10px;
                    }
                    .content-form p {
                        color: #777;
                        margin-bottom: 25px;
                    }
                    .form-group {
                        display: flex;
                        flex-direction: column;
                        gap: 15px;
                    }
                    input[type="url"] {
                        padding: 15px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        font-size: 1em;
                        width: calc(100% - 30px);
                    }
                    button[type="submit"] {
                        padding: 15px;
                        font-size: 1em;
                        width: 100%;
                    }
                    .message {
                        margin-top: 20px;
                        font-weight: bold;
                        font-size: 1.1em;
                    }
                    .success {
                        color: green;
                    }
                    .error {
                        color: red;
                    }
                    .footer {
                        background-color: var(--dark-gray);
                        color: var(--footer-text);
                        text-align: center;
                        padding: 10px;
                        font-size: 0.9em;
                        width: 100%;
                        position: relative;
                    }
                `
            }} />
            <header className="navbar">
                <div className="logo">Strydo</div>
                <ul className="navbar-links">
                    <Link to="/link">Link to Content</Link>
                    <Link to="/post">Text to Content</Link>
                </ul>
                <Link to="/post" className="btn btn-primary">Go Back</Link>
            </header>
            <main className="main-content">
                <div className="content-form">
                    <h1>Post content from a URL</h1>
                    <p>Enter the URL of an article or blog post and our AI will summarize it and auto-post it for you.</p>
                    <form onSubmit={handleSubmit} className="form-group">
                        <input
                            type="url"
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            placeholder="Enter article URL"
                        />
                        <button type="submit" className="btn btn-primary" disabled={isLoading}>
                            {isLoading ? 'Processing...' : 'Run Agent'}
                        </button>
                    </form>
                    {message && (
                        <p className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
                            {message}
                        </p>
                    )}
                </div>
            </main>
            <footer className="footer">
                <div className="container">
                    <p>© 2025 Strydo All rights reserved.</p>
                </div>
            </footer>
        </div>
        </>
    );
};

export default LinkToContent;