import { FC } from 'react';

import { CircularProgress } from '@mui/material';
import css from './Loader.module.scss';

const Loader: FC = () => {
  return (
    <div className={css.loader}>
      <CircularProgress style={{ color: '#111d13' }} />
    </div>
  );
};

export { Loader };
