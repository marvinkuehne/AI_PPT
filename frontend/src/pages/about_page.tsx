import Logo from '../assets/logo.svg'

function AboutPage() {
  return (
      <div className='flex h-full flex-col justify-center items-center'>
        <img src={Logo} alt='logo' className='w-16 h-16 mb-4' />
        <h1 className='bold text-3xl'>MagicPPT</h1>
        <h2>Version: 1.0.0</h2>
      </div>
  );
}

export default AboutPage;