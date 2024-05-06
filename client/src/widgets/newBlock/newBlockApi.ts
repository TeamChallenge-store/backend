import { baseApi } from '~shared/api/baseApi';

import { IProductCard, TResponse } from '~entities/product/model/types';

export const productApi = baseApi.injectEndpoints({
  endpoints: build => ({
    newProduct: build.query<IProductCard[], void>({
      query: () => 'products/?sort=date',
      keepUnusedDataFor: 30,
      transformResponse: (response: TResponse) => response.results,
    }),
  }),
});

export const { useNewProductQuery } = productApi;
