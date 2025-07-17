import Footer from "./_components/footer";
import OurCreation from "./_components/our-creation";

type Props = {
  children: React.ReactNode;
};

const HomeLayout = ({ children }: Props) => {
  return (
    <div>
      {children}
      <OurCreation />
      <Footer />
    </div>
  );
};

export default HomeLayout;
