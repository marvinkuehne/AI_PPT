import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {RouterProvider, Outlet, createHashRouter} from "react-router";
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import {routes} from "./routes.tsx";
import App from "./App.tsx";

function _Layout() {
  return (
      <DashboardLayout>
        <div className="p-6 h-full">
          <Outlet />
        </div>
      </DashboardLayout>
  );
}

const router = createHashRouter([
  {
    element: <App />,
    children: [
      {
        path: '/',
        element: <_Layout />,
        children: routes
      },
    ]
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
