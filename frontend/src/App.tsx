import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import NewPrescription from './pages/NewPrescription';
import Dashboard from './pages/Dashboard';
import PrescriptionHistory from './pages/PrescriptionHistory';
import PrintView from './pages/PrintView';
import CrudPage from './pages/CrudPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          {/* Default landing: New Prescription */}
          <Route path="/" element={<NewPrescription />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/prescriptions" element={<PrescriptionHistory />} />
          <Route path="/prescriptions/:id" element={<PrintView />} />

          {/* Master Data CRUD pages */}
          <Route path="/illnesses" element={<CrudPage resource="illnesses" title="Illnesses" />} />
          <Route path="/medicines" element={<CrudPage resource="medicines" title="Medicines List" />} />
          <Route path="/patients" element={<CrudPage resource="patients" title="Patients" />} />
          <Route path="/lab-tests" element={<CrudPage resource="lab-tests" title="Lab Tests" />} />
          <Route path="/symptoms" element={<CrudPage resource="symptoms" title="Symptoms" />} />
          <Route path="/referral-doctors" element={<CrudPage resource="referral-doctors" title="Referral Doctors" />} />
          <Route path="/advice-templates" element={<CrudPage resource="advice-templates" title="Advice Templates" />} />
          <Route path="/prescription-templates" element={<CrudPage resource="prescription-templates" title="Prescription Templates" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
