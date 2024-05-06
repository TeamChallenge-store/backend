import { FC } from 'react';

import css from './ProductListFilters.module.scss';

type TProductListFiltersProps = object;

const ProductListFilters: FC<TProductListFiltersProps> = () => {
  return (
    <div className={css.inner}>
      Filters
      <svg
        className={css.icon}
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M4 12H14.1M4 6H20M4 18H11.1"
          stroke="#A0A0A0"
          strokeWidth="1.6"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
};

export { ProductListFilters };
