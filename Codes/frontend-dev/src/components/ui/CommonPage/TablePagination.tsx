import { FC, memo } from 'react';
export interface PaginationProps {
  pagination: (val: number) => void;
  totaldata: number;
  tableTake: number;
  pageSelected: number;
}

const TablePagination: FC<PaginationProps> = ({
  pagination,
  totaldata,
  tableTake,
  pageSelected,
}) => {
  const noOfPages = Math.ceil(totaldata / tableTake);
  const arr = [...new Array(noOfPages).keys()];
  const startIndex = (pageSelected - 1) * tableTake + 1;
  const endIndex =
    arr.length === pageSelected ? totaldata : pageSelected * tableTake;

  if (noOfPages <= 1) return <> </>;
  return (
    <div className="bg-white py-3 flex items-center justify-between border-t border-gray-200">
      <div className="flex-1 flex justify-between sm:hidden">
        <label className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
          {' '}
          Previous{' '}
        </label>
        <label className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
          {' '}
          Next{' '}
        </label>
      </div>
      <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p className="text-sm text-gray-700">
            Showing
            <span className="font-medium"> {startIndex} </span>
            to
            <span className="font-medium"> {endIndex} </span>
            of
            <span className="font-medium"> {totaldata} </span>
            results
          </p>
        </div>
        <div>
          <nav
            className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
            aria-label="Pagination"
          >
            <button
              type="button"
              onClick={() => pagination(pageSelected - 2)}
              className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 cursor-pointer"
              disabled={pageSelected === 1}
            >
              <span className="sr-only">Previous</span>
              <svg
                className="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
            {arr.map((i: number) => {
              return (
                <label
                  key={i}
                  onClick={() => pagination(i)}
                  aria-current="page"
                  className={
                    pageSelected === i + 1
                      ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600 relative inline-flex items-center px-4 py-2 border text-sm font-medium cursor-pointer'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50 hidden md:inline-flex relative items-center px-4 py-2 border text-sm font-medium cursor-pointer'
                  }
                >
                  {' '}
                  {i + 1}{' '}
                </label>
              );
            })}

            {/* <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
              {' '}
              ...{' '}
            </span> */}
            <button
              type="button"
              onClick={() => pagination(pageSelected)}
              className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
              disabled={endIndex === totaldata}
            >
              <span className="sr-only">Next</span>
              <svg
                className="h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                aria-hidden="true"
              >
                <path
                  fillRule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </button>
          </nav>
        </div>
      </div>
    </div>
  );
};

export default memo(TablePagination);
