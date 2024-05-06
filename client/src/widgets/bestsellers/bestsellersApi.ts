import { baseApi } from '~shared/api/baseApi';

import { IProductCard, TResponse } from '~entities/product/model/types';

export const productApi = baseApi.injectEndpoints({
  endpoints: build => ({
    bestsellersProduct: build.query<IProductCard[], void>({
      query: () => 'products/?sort=rate',
      keepUnusedDataFor: 30,
      transformResponse: (response: TResponse) => response.results,
    }),
  }),
});

export const { useBestsellersProductQuery } = productApi;
