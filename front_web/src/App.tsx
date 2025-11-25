import { Routes, Route } from 'react-router-dom';
import MainPage from './pages/MainPage';
import SettingPage from './pages/SettingPage';
import AnalyzePage from './pages/AnalyzePage';
import ResultPage from './pages/ResultPage';
import NavHeader from './components/StyledNavHeader';
import ReportPage from './pages/ReportPage';

function App() {
  return (
    <>
    <Routes>
      <Route path ="/" element = {<MainPage/>}/>
      <Route path ="/main" element = {<MainPage/>}/>
      <Route 
        path = "/analyze" 
        element = {
          <>
            <NavHeader title="Detect Finished" /> 
            <AnalyzePage/>
          </>
        }
      />
      <Route 
        path = "/result" 
        element = {
          <>
            <NavHeader title="Detection Result" />
            <ResultPage/>
          </>
        }
      />
      <Route
        path = "/report"
        element = {
          <>
          <NavHeader title = "Detect Finished" />
          <ReportPage/>
          </>
        }
        />
      <Route 
        path ="/setting" 
        element = {
          <>
            <NavHeader title="Settings" />
            <SettingPage/>
          </>
        }
      />
      
      <Route path ="*" element={<h1>404 Not Found</h1>}/>
    </Routes>
      
    </>
  )
}

export default App