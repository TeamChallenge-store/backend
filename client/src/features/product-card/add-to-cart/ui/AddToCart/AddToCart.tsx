import { useEffect, useState } from 'react';
import { LoadingButton } from '@mui/lab';
import { ThemeProvider } from '@mui/material';
import cn from 'classnames';

import theme from '../../config/muiTheme';

import css from './AddToCart.module.scss';

const AddToCart = () => {
  const [isLiked, setIsLiked] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [count, setCount] = useState(1);
  const [timeoutId, setTimeoutId] = useState<number | undefined>(undefined);

  const handleClick = () => {
    setIsLiked(!isLiked);
    setLoading(true);

    const id = setTimeout(() => {
      setLoading(false);
    }, 500);

    setTimeoutId(+id);
  };

  useEffect(
    () => () => {
      clearTimeout(timeoutId);
    },
    [timeoutId],
  );

  return (
    <ThemeProvider theme={theme}>
      <div className={css.addButtonContainer}>
        <div
          className={cn(css.controlButton, {
            [css.hidden]: isLiked,
          })}
        >
          <button
            className={css.left}
            onClick={() => {
              if (count <= 1) {
                return;
              }

              setCount(prev => prev - 1);
            }}
            type="button"
          >
            -
          </button>
          <span className={css.count}>{count}</span>
          <button
            className={css.right}
            onClick={() => setCount(prev => prev + 1)}
            type="button"
          >
            +
          </button>
        </div>
        <LoadingButton
          onClick={handleClick}
          disabled={isLiked}
          loading={isLoading}
          variant="contained"
        >
          {!isLiked && (
            <svg
              className={css.cartSvg}
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                // eslint-disable-next-line max-len
                d="M8.25 8.25V6C8.25 5.40326 8.48705 4.83097 8.90901 4.40901C9.33097 3.98705 9.90326 3.75 10.5 3.75H13.5C14.0967 3.75 14.669 3.98705 15.091 4.40901C15.5129 4.83097 15.75 5.40326 15.75 6C15.75 6.59674 15.5129 7.16903 15.091 7.59099C14.669 8.01295 14.0967 8.25 13.5 8.25H3.75V16.5C3.75 17.4946 4.14509 18.4484 4.84835 19.1517C5.55161 19.8549 6.50544 20.25 7.5 20.25H16.5C17.4946 20.25 18.4484 19.8549 19.1517 19.1517C19.8549 18.4484 20.25 17.4946 20.25 16.5V8.25H17.5"
                stroke="white"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
          )}
          {isLiked && !isLoading && (
            <svg
              className={css.cartCheck}
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <rect
                x="0.75"
                y="0.75"
                width="18.5"
                height="18.5"
                rx="9.25"
                stroke="white"
                strokeWidth="1.5"
              />
              <path
                // eslint-disable-next-line max-len
                d="M8.44214 11.8837L6.75534 10.1969C6.66452 10.1059 6.54122 10.0547 6.41263 10.0547C6.28405 10.0547 6.16074 10.1059 6.06992 10.1969C5.88034 10.3865 5.88034 10.6927 6.06992 10.8823L8.10187 12.9143C8.29145 13.1038 8.5977 13.1038 8.78728 12.9143L13.9303 7.7712C14.1199 7.58162 14.1199 7.27537 13.9303 7.08578C13.8395 6.99476 13.7162 6.9436 13.5876 6.9436C13.459 6.9436 13.3357 6.99476 13.2449 7.08578L8.44214 11.8837Z"
                fill="white"
              />
            </svg>
          )}
        </LoadingButton>
      </div>
    </ThemeProvider>
  );
};

export { AddToCart };
