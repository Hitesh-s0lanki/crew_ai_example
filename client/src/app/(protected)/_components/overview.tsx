import Image from "next/image";

type Props = {
  title: string;
  description: string;
  image: string;
};

const Overview = ({ title, description, image }: Props) => {
  return (
    <div className="w-full flex flex-col justify-center items-center px-8 md:px-10 lg:px-20">
      <div className="w-full rounded-2xl ">
        <div className="flex flex-col items-center justify-center text-center py-5 rounded-[15px]">
          {/* Title */}
          <h2 className="text-2xl font-semibold mt-2">
            Meet the <br />
            <span className="bg-gradient-to-r from-primary to-red-400 bg-clip-text text-transparent text-4xl">
              {title}
            </span>
          </h2>

          {/* Description */}
          <p className="text-slate-500 mt-2 max-w-full md:text-lg md:px-5 lg:px-10">
            {description}
          </p>

          <Image
            src={image}
            alt="financial researcher"
            height={700}
            width={800}
            className="mt-5"
          />
        </div>
      </div>
    </div>
  );
};

export default Overview;
