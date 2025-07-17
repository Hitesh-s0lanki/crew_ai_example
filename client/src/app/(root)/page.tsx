import Hero from "./_components/hero";
import Navbar from "./_components/navbar";

const HomePage = () => {
  return (
    <div className="bg-[url('https://raw.githubusercontent.com/prebuiltui/prebuiltui/main/assets/hero/gridBackground.png')] w-full bg-no-repeat bg-cover bg-center text-sm pb-44 min-h-screen">
      <Navbar />
      <Hero />
    </div>
  );
};

export default HomePage;
