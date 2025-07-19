import MainScreen from "./_components/main-screen";

type Props = {
  params: Promise<{ id: string }>;
};

const CrewPage = async ({ params }: Props) => {
  const paramsObj = await params;

  if (!paramsObj.id) {
    return <div>No ID provided</div>;
  }

  return <MainScreen id={paramsObj.id} />;
};

export default CrewPage;
