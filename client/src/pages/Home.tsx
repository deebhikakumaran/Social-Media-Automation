import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <>
      <meta charSet="utf-8" />
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" />
      
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
            .hero {
                background: linear-gradient(180deg, var(--orange-gradient-top), var(--orange-gradient-bottom));
                background-repeat: no-repeat;
                padding: 80px 20px 0;
                color: var(--text-light);
                position: relative;
            }
            .hero-flex-container {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .hero-image-container {
                flex-basis: 350px;
                text-align: left;
            }
            .hero-text-content {
                flex: 1;
                text-align: right;
                padding-left: 20px;
            }
            .hero h1 {
                font-size: 3.5em;
                font-weight: 700;
                margin-bottom: 10px;
            }
            .hero p {
                max-width: 600px;
                margin: 0 0 30px auto;
                font-size: 1.2em;
            }
            .hero-image {
                width: 350px;
                height: 450px;
            }
            .testimonials {
                background-color: var(--light-gray-bg);
                padding: 60px 20px;
                text-align: center;
            }
            .testimonials h2 {
                font-size: 2.5em;
                margin-bottom: 5px;
                color: var(--orange-gradient-bottom);
                font-weight: 600;
            }
            .testimonials .sub-heading {
                font-size: 1.1em;
                margin-bottom: 20px;
                color: #666;
            }
            .testimonials h3 {
                font-size: 1.8em;
                color: var(--border-orange);
                font-weight: 600;
            }
            .testimonial-cards {
                display: flex;
                justify-content: center;
                gap: 25px;
                flex-wrap: wrap;
                margin-top: 40px;
            }
            .testimonial-card {
                background-color: var(--quote-bg);
                border: 2px solid var(--border-orange);
                border-radius: 10px;
                padding: 30px;
                max-width: 250px;
                text-align: left;
            }
            .testimonial-card p {
                font-style: italic;
                line-height: 1.6;
            }
            .testimonial-card .author {
                margin-top: 20px;
                font-weight: 600;
                font-style: normal;
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
        <header className="navbar">
          <div className="logo">Strydo</div>
          <ul className="navbar-links"> 
            <Link to="/link">Link to Content</Link>
            <Link to="/post">Text to Content</Link>
          </ul>
          <Link to="/post" className="btn btn-primary">Start for free</Link>
        </header>
        <main className="flex-1">
          <section className="hero">
            <div className="container">
              <div className="hero-flex-container">
                <div className="hero-image-container">
                  <img src="/robot.png" alt="Strydo AI Robot" className="hero-image" />
                </div>
                <div className="hero-text-content">
                  <h1>Never miss a post again</h1>
                  <p>Strydo is the AI co-pilot that helps creators generate consistent, high-quality content for every channel.</p>
                  <Link to="/post" className="btn btn-primary">Start Your Momentum Now</Link>
                </div>
              </div>
            </div>
          </section>
          <section className="testimonials">
            <div className="container">
              <h2>Stop chasing algorithms, start building your audience</h2>
              <p className="sub-heading">See what other creators are saying about Strydo.</p>
              <div className="testimonial-cards">
                <div className="testimonial-card">
                  <p>"Strydo has transformed my content strategy. My engagement has skyrocketed."</p>
                  <p className="author">- Sarah, Content Creator</p>
                </div>
                <div className="testimonial-card">
                  <p>"I used to spend hours brainstorming. Now Strydo gives me endless ideas and is a game-changer for my productivity."</p>
                  <p className="author">- Mike, YouTuber</p>
                </div>
                <div className="testimonial-card">
                  <p>"The quality of the content suggestions perfectly captures my brand. I highly recommend it."</p>
                  <p className="author">- Jessica, Blogger</p>
                </div>
              </div>
            </div>
          </section>
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

export default Home;