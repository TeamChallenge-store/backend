import { FC } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination } from 'swiper/modules';
import { ProductList } from '~widgets/product-list';
import { CustomButton } from '~shared/ui/CustomButton';
import { useSaleProductsQuery } from './promotionalOffersApi';

import 'swiper/css';
import css from './PromotionalOffers.module.scss';
import { Loader } from '~shared/ui/Loader';

const PromotionalOffers: FC = () => {
  const { data: products, isLoading } = useSaleProductsQuery();

  if (isLoading) {
    return <Loader />;
  }

  return (
    <div className={css.offers}>
      <div className={css.offersBunner}>
        <div className={css.offersBunnerContent}>
          <span className={css.offersSubtitle}>Shoes and jackets</span>
          <h3 className={css.offersTitle}>Final sale up to 30%</h3>
          <p className={css.offersDescription}>
            Final сlearance on apparel and footwear
          </p>
          <CustomButton to="/sale" bgColor="white" className={css.offersLink}>
            see more
            <svg
              width="25"
              height="24"
              viewBox="0 0 25 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                // eslint-disable-next-line max-len
                d="M8.64239 6.43312L18.1442 7.34961L17.2277 16.8515M17.4207 7.94582L6.8577 16.6504"
                stroke="rgba(17, 29, 19, 1)"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </CustomButton>
        </div>
      </div>
      <div className={`${css.offersSlider} container`}>
        <Swiper
          slidesPerView={4}
          spaceBetween={15}
          navigation={{
            prevEl: '#swiper-prev',
            nextEl: '#swiper-next',
          }}
          breakpoints={{
            375: {
              slidesPerView: 2,
            },
            500: {
              slidesPerView: 2,
              spaceBetween: 15,
            },
            767: {
              slidesPerView: 3,
            },
            1025: {
              slidesPerView: 4,
              spaceBetween: 20,
            },
            1440: {
              spaceBetween: 25,
            },
          }}
          modules={[Navigation, Pagination]}
          className={`swiper-wrapper ${css.swiperWrapper}`}
        >
          {
            // eslint-disable-next-line operator-linebreak
            products &&
              products.map(product => (
                <SwiperSlide
                  key={product.id}
                  className={`${css.swiperSlide} swiper-slide`}
                >
                  <div className={css.imageInner}>
                    <ProductList products={[product]} />
                  </div>
                </SwiperSlide>
              ))
          }
        </Swiper>
        <div className={css.swiperNavigationArrows}>
          <CustomButton
            id="swiper-prev"
            className={`swiper-prev ${css.swiperPrev} `}
            bgColor="white"
          >
            <svg
              width="19.94"
              height="20.85"
              viewBox="0 0 22 21"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                // eslint-disable-next-line max-len
                d="M10.2929 19.0977L1.82227 10.6271L10.2929 2.15648M2.99874 10.6271L20.1752 10.6271"
                stroke="#111D13"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </CustomButton>
          <CustomButton
            id="swiper-next"
            className={`swiper-next ${css.swiperNext}`}
            bgColor="white"
          >
            <svg
              width="19.94"
              height="20.85"
              viewBox="0 0 22 21"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                // eslint-disable-next-line max-len
                d="M10.2929 19.0977L1.82227 10.6271L10.2929 2.15648M2.99874 10.6271L20.1752 10.6271"
                stroke="#111D13"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </CustomButton>
        </div>
      </div>
    </div>
  );
};

export { PromotionalOffers };
