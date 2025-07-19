import MainScreen from "./_components/main-screen";

type Props = {
  params: { id: string };
};

const CrewPage = async ({ params }: Props) => {
  const { id } = await params;

  return <MainScreen id={id} />;
};

export default CrewPage;
