import { FC } from 'react';
import Image from 'next/image';
import NoData from 'assets/nodata-icon.png';
import { useRouter } from 'next/router';

export const NoRecords: FC = () => {
  const router = useRouter();
  return (
    <div className="ml-20 p-10 h-screen overscroll-y-auto ">
      <div className="px-6 py-16 bg-white rounded-lg mt-6 mb-10 text-center">
        <div className="">
          <Image src={NoData} alt="404" className="inline-block w-24" />
        </div>
        <h1 className="text-2xl font-bold p-3 mt-5">No Data Found</h1>
        <p className="pb-5">Oh no, bad luck!</p>
        <button
          onClick={() => router.push('home')}
          className="transition-all border-2 w-auto inline-block border-sky-600 p-2 px-10 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  hover:bg-sky-700"
        >
          Go to Home
        </button>
      </div>

      <div className="clear-both" />
    </div>
  );
};
