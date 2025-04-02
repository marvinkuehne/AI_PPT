import {Navigate, RouteObject} from "react-router";
import AboutPage from "./pages/about_page.tsx";
import SettingsPage from "./pages/settings_page.tsx";
import ProfilePage from "./pages/profile_page.tsx";
import FilesPage from "./pages/files_page.tsx";
import ConverterPage from "./pages/converter_page.tsx";

export const routes: RouteObject[] = [
  {
    path: '',
    element: <Navigate to='/new' />,
  },
  {
    path: 'new',
    element: <ConverterPage />
  },
  {
    path: 'files',
    element: <FilesPage />
  },
  {
    path: 'profile',
    element: <ProfilePage />
  },
  {
    path: 'settings',
    element: <SettingsPage />
  },
  {
    path: 'about',
    element: <AboutPage />
  },
  {
    path: '*',
    element: <Navigate to='/new' />
  },
]