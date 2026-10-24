import { NavLink, Outlet } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'New Prescription', icon: '✏️', end: true },
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/prescriptions', label: 'Prescription History', icon: '📋' },
];

const masterDataItems = [
  { to: '/illnesses', label: 'Illnesses', icon: '🦠' },
  { to: '/medicines', label: 'Medicines', icon: '💊' },
  { to: '/patients', label: 'Patients', icon: '👤' },
  { to: '/lab-tests', label: 'Lab Tests', icon: '🧪' },
  { to: '/symptoms', label: 'Symptoms', icon: '🌡️' },
  { to: '/referral-doctors', label: 'Referral Doctors', icon: '👨‍⚕️' },
  { to: '/advice-templates', label: 'Advice Templates', icon: '📝' },
  { to: '/prescription-templates', label: 'Rx Templates', icon: '📄' },
];

export default function Layout() {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-60 shrink-0 border-r border-slate-200 bg-slate-50 flex flex-col overflow-y-auto">
        {/* Logo */}
        <div className="flex items-center gap-2 px-4 py-4 border-b border-slate-200">
          <div className="w-9 h-9 rounded-lg flex items-center justify-center text-white font-bold text-lg bg-clinic-600">
            +
          </div>
          <div>
            <div className="text-sm font-bold text-slate-800">Clinic App</div>
            <div className="text-xs text-slate-400">Prescriptions</div>
          </div>
        </div>

        {/* Main nav */}
        <nav className="flex-1 px-3 py-3 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-clinic-100 text-clinic-700 font-semibold'
                    : 'text-slate-600 hover:bg-slate-100'
                }`
              }
            >
              <span>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}

          {/* Master Data section */}
          <div className="pt-5 pb-1 px-3 text-xs uppercase tracking-wide text-slate-400 font-medium">
            Master Data
          </div>
          {masterDataItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-2.5 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-clinic-100 text-clinic-700 font-semibold'
                    : 'text-slate-600 hover:bg-slate-100'
                }`
              }
            >
              <span>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex-1 overflow-y-auto bg-slate-100">
        <Outlet />
      </div>
    </div>
  );
}
