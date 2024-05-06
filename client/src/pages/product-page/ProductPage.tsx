import { useSearchParams } from 'react-router-dom';

import { ProductList } from '~widgets/product-list';
import { ProductListFilters } from '~features/product-list';
import { useProductCategoryQuery } from '~entities/product';
import { CustomSelect } from '~shared/ui/CustomSelect';

import { Layout } from './ui/Layout';
import options from './model/selectOptions';
import {
  QUERY_NAME,
  DEFAULT_SORT_PARAM,
  DEFAULT_SORT_LABLE,
} from './constants';

const ProductPage = () => {
  const [searchParams] = useSearchParams();
  const { data: products, isLoading } = useProductCategoryQuery(
    searchParams.get(QUERY_NAME)?.toString() ?? DEFAULT_SORT_PARAM,
  );

  if (isLoading) {
    return 'Loading';
  }

  if (!products) {
    return 'no category';
  }

  return (
    <Layout
      sidebar={null}
      sortBy={
        <CustomSelect options={options} startValue={DEFAULT_SORT_LABLE} />
      }
      filtersMob={<ProductListFilters />}
      productList={<ProductList products={products} />}
      pagination={null}
    />
  );
};

export { ProductPage };
