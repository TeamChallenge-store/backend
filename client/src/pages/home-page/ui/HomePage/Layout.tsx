import { FC, ReactNode } from 'react';
import cn from 'classnames';

import css from './Layout.module.scss';

type TLayoutProps = {
  banner?: ReactNode;
  bestsellers?: ReactNode;
  subCategory?: ReactNode;
  newProducts?: ReactNode;
  stock?: ReactNode;
  subscribe?: ReactNode;
};

const Layout: FC<TLayoutProps> = props => {
  return (
    <>
      <section className={cn(css.banner)}>{props.banner}</section>
      <section className={cn(css.bestsellers, 'container')}>
        {props.bestsellers}
      </section>
      <section className={cn(css.subCategory, 'container')}>
        {props.subCategory}
      </section>
      <section className={cn(css.newProducts, 'container')}>
        {props.newProducts}
      </section>
      <section className={css.stock}>{props.stock}</section>
      <section className={cn(css.subscribe)}>{props.subscribe}</section>
    </>
  );
};

export { Layout };
