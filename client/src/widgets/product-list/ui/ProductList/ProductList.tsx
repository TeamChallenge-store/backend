import { FC } from 'react';
import { type IProductCard } from '~entities/product';

import { AddToCart, AddToWish } from '~features/product-card';
import { LayoutProductCard } from '~shared/ui/LayoutProductCard';

type TProductListProps = {
  products: IProductCard[];
};

const ProductList: FC<TProductListProps> = ({ products }) => {
  return products.map(product => (
    <LayoutProductCard
      key={product.id}
      product={product}
      addToCartSlot={<AddToCart />}
      wishSlot={<AddToWish />}
    />
  ));
};

export { ProductList };
