import { FC } from 'react';
import { useRouter } from 'next/router';
import Image from 'next/image';
import Logo from 'assets/logo.svg';
import PageNotFound from 'assets/page-404.png';

export const ErrorPage: FC = () => {
  const router = useRouter();
  return (
    <div className="w-full p-5 text-center lg:p-10">
      <div className="mt-2">
        <Image src={Logo} alt="Logo" className="inline-block w-44" />
      </div>
      <div className="pt-10">
        <Image src={PageNotFound} alt="404" className="inline-block w-54" />
      </div>
      <h1 className="text-3xl font-bold p-3 mt-5">Page Not Found</h1>
      <p className="pb-5">Oh no, bad luck!</p>
      <button
        onClick={() => router.push('home')}
        className="transition-all border-2 w-auto inline-block border-sky-600 p-2 px-10 rounded-lg text-white text-base font-semibold ml-0 bg-sky-600 lg:my-0  hover:bg-sky-700"
      >
        Go to Home
      </button>
    </div>
  );
};
