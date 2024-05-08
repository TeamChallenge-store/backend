import { FC } from 'react';
import { useDebounce } from 'use-debounce';
import { NavLink } from 'react-router-dom';
import cn from 'classnames';
import { useSearchProductsQuery } from '~entities/product';
import css from './SearchResults.module.scss';

type TSearchResultsProps = {
  searchText: string;
  className: string;
  isExpanded: boolean;
  handleFormClose: () => void;
};

const SearchResults: FC<TSearchResultsProps> = ({
  searchText,
  className,
  isExpanded,
  handleFormClose,
}) => {
  const getSearchQuery = searchText.length > 0 ? searchText : '';
  const getDebouncedSearchQuery = useDebounce(getSearchQuery, 500);

  const {
    data: products,
    isLoading,
    error,
  } = useSearchProductsQuery(getDebouncedSearchQuery[0]);

  if (isLoading && isExpanded) {
    return <div className={css.loading}>Loading...</div>;
  }

  if ((error || products?.length === 0) && isExpanded) {
    return (
      <div className={css.errorMessage}>Sorry, your item was not found</div>
    );
  }

  return (
    isExpanded && (
      <div className={cn(className)}>
        {products && products.length > 0 && !isLoading && !error && (
          <>
            <NavLink
              to="/allProducts"
              className={css.link}
              onClick={handleFormClose}
            >
              All search results
            </NavLink>
            {products?.slice(0, 5)?.map(product => (
              <NavLink
                key={product.id}
                to={`${product.id}`}
                className={css.link}
                onClick={handleFormClose}
              >
                {product.name}
              </NavLink>
            ))}
          </>
        )}
      </div>
    )
  );
};

export { SearchResults };
