import { Routes, Route } from 'react-router-dom';
import MainPage from '../src/pages/MainPage';
import SettingPage from '../src/pages/SettingPage';

function App() {
  return (
    <>
    <Routes>
      <Route path ="/" element = {<MainPage/>}/>
      <Route path ="/main" element = {<MainPage/>}/>
      <Route path ="/setting" element = {<SettingPage/>}/>
      <Route path ="*" element={<h1>404 Not Found</h1>}/>
    </Routes>
      
    </>
  )
}

export default App
