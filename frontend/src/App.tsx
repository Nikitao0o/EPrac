import { Navigate, Route, Routes } from 'react-router-dom'
import { Layout } from './components/Layout'
import { SearchPage } from './pages/SearchPage'
import { UploadPage } from './pages/UploadPage'
import './App.css'

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Navigate to="/upload" replace />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/search" element={<SearchPage />} />
      </Route>
    </Routes>
  )
}

export default App
