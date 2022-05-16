import { FC, useState } from 'react';
import { ValidationMessage } from './ValidationMessage';
import { useSession } from '@lib/useSession';

interface DateProps {
  submitDates: () => void;
}

export const DateRangePicker: FC<DateProps> = ({ submitDates }) => {
  const { state, dispatch } = useSession();
  const { dateRange } = state;
  const [validationMessage, setValidationMessage] = useState<string>('');

  const validateDates = () => {
    if (new Date(dateRange.from).getTime() > new Date(dateRange.to).getTime()) {
      setValidationMessage(
        'Please select a from-date which is earlier than to-date',
      );
    } else {
      setValidationMessage('');
      submitDates();
    }
  };

  const updateDate = (from: string, to: string) => {
    dispatch({
      type: 'dateSelection',
      dateRange: { from, to },
    });
  };

  return (
    <>
      <div
        date-rangepicker
        className="w-full flex items-center relative float-right date-style"
      >
        <div className="relative w-full">
          <input
            name="start"
            type="date"
            className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-1 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 cursor-pointer"
            placeholder="Select date start"
            value={dateRange.from}
            onChange={e => updateDate(e.target.value, dateRange.to)}
          />
        </div>
        <span className="mx-4 text-gray-500">to</span>
        <div className="relative w-full">
          <input
            name="end"
            type="date"
            className="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pl-1 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 cursor-pointer"
            placeholder="Select date end"
            value={dateRange.to}
            onChange={e => updateDate(dateRange.from, e.target.value)}
            max={dateRange.to}
          />
        </div>
        <button
          type="button"
          className="px-5 py-2 float-right bg-sky-600 rounded-md text-white font-medium"
          onClick={() => validateDates()}
        >
          Submit
        </button>
      </div>
      <ValidationMessage message={validationMessage} />
    </>
  );
};
