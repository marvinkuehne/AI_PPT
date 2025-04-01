import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import {createBrowserRouter, RouterProvider, Outlet} from "react-router";
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import AppMenu from "./components/AppMenu.tsx";
import {routes} from "./routes.tsx";

function _Layout() {
  return (
      <DashboardLayout>
        <div className="p-6 h-full">
          <Outlet />
        </div>
      </DashboardLayout>
  );
}

const router = createBrowserRouter([
  {
    element: <AppMenu />,
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
