import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import './App.css';
import './styles/themes.css';
import './styles/components.css';
import Inference from './pages/Inference';

function App() {

  return (
    
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="/inference/:model_name/:task_name" element={<Inference />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App
