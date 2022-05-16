import { Dispatch, memo, SetStateAction, useEffect, FC } from 'react';

type SnackbarType = {
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
  message: string;
  type: string;
};

const CustomizedSnackbars: FC<SnackbarType> = ({
  open,
  setOpen,
  message,
  type,
}: SnackbarType) => {
  const color = type === 'success' ? '#6da844' : 'rgb(211, 47, 47)';
  const toast = open === true ? 'block' : 'none';

  useEffect(() => {
    if (open) {
      setTimeout(() => {
        setOpen(false);
      }, 5000);
    }
  }, [open, setOpen]);

  return (
    <>
      <div style={{ display: toast }}>
        <div className="sticky_bar_outer" style={{ backgroundColor: color }}>
          {message}
        </div>
      </div>
    </>
  );
};

export default memo(CustomizedSnackbars);
