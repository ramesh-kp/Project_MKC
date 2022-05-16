import { FC, memo } from 'react';

const ApiLoaderComponent: FC = () => {
  return (
    <>
      <div className="flex items-center justify-center">
        <div className=" top-52 fixed z-50">
          <button
            type="button"
            className="inline-flex items-center px-8 py-4 font-semibold leading-6 text-lg shadow rounded-lg text-black bg-white transition ease-in-out duration-150"
            disabled={undefined}
          >
            <svg
              className="animate-spin -ml-1 mr-3 h-16 w-16 text-sky-600"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth={2}
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Processing...
          </button>
        </div>
      </div>
      <div className="fixed bg-current left-0 top-0 opacity-40 z-30 w-full h-full" />
    </>
  );
};

export const ApiLoader = memo(ApiLoaderComponent);
