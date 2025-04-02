import { createTheme } from '@mui/material/styles';
import {Branding, type Navigation} from '@toolpad/core/AppProvider';
import {ReactRouterAppProvider} from "@toolpad/core/react-router";
import {Outlet} from "react-router";
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import BackupTableIcon from '@mui/icons-material/BackupTable';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SettingsIcon from '@mui/icons-material/Settings';
import InfoOutlineIcon from '@mui/icons-material/InfoOutline';
import Logo from '../assets/logo.svg'

const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Services',
  },
  {
    segment: 'new',
    title: 'Converter',
    icon: <AutoFixHighIcon />,
  },
  {
    segment: 'files',
    title: 'Files',
    icon: <BackupTableIcon />,
  },
  {
    kind: 'header',
    title: 'Account',
  },
  {
    segment: 'profile',
    title: 'Profile',
    icon: <AccountCircleIcon />,
  },
  {
    segment: 'settings',
    title: 'Settings',
    icon: <SettingsIcon />,
  },
  {
    kind: 'header',
    title: 'Info',
  },
  {
    segment: 'about',
    title: 'About',
    icon: <InfoOutlineIcon />,
  },
];

const BRANDING: Branding = {
  title: 'MagicPPT',
  logo: <img src={Logo} alt='logo' className='w-6 flex h-full justify-center items-center' />,
};

const demoTheme = createTheme({
  cssVariables: {
    colorSchemeSelector: 'data-toolpad-color-scheme',
  },
  colorSchemes: { light: true, dark: true },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 600,
      lg: 1200,
      xl: 1536,
    },
  },
});

export default function AppMenu() {
  return (
      <ReactRouterAppProvider
          navigation={NAVIGATION}
          branding={BRANDING}
          theme={demoTheme}
      >
        <Outlet />
      </ReactRouterAppProvider>
  );
}