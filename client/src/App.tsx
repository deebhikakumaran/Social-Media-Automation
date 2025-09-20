import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Post from './pages/Post';
import LinkToContent from './pages/LinkToContent';

function App() {

  return (
    <>
      <BrowserRouter> 
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/post" element={<Post />} />
          <Route path="/link" element={<LinkToContent />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
