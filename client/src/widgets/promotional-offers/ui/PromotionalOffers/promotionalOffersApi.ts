import { baseApi } from '~shared/api/baseApi';

import { IProductCard, TResponseProducts } from '~entities/product/model/types';

export const productApi = baseApi.injectEndpoints({
  endpoints: build => ({
    saleProducts: build.query<IProductCard[], void>({
      query: () => 'product-categories/sale',
      keepUnusedDataFor: 30,
      transformResponse: (response: TResponseProducts) =>
        response.results.products,
    }),
  }),
});

export const { useSaleProductsQuery } = productApi;
