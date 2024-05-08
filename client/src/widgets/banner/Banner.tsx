import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, Scrollbar, Navigation, Pagination } from 'swiper/modules';
import { BannerInfo } from '~features/bannerInfo';

import tent from '~shared/tent.jpg';
import mountainView from './bannerImg/mountainView.jpg';
import people from './bannerImg/people.jpg';

import css from './Banner.module.scss';
import 'swiper/css';

const Banner = () => {
  return (
    <>
      <div className={css.bannerSwiper}>
        <Swiper
          spaceBetween={0}
          slidesPerView={1}
          autoplay={{
            delay: 2000,
          }}
          speed={600}
          pagination={{
            clickable: true,
            el: '#Banner',
            bulletClass: `swiper-pagination-bullet ${css.swiperPaginationBullet}`,
            bulletActiveClass: `swiper-pagination-bullet-active ${css.swiperPaginationBulletActive}`,
          }}
          navigation={{
            prevEl: '#BannerBtnPrev',
            nextEl: '#BannerBtnNext',
          }}
          loop
          modules={[Autoplay, Scrollbar, Navigation, Pagination]}
        >
          <SwiperSlide>
            <div className={css.bannerImg}>
              <img src={mountainView} alt="mountain" />
            </div>
            <BannerInfo />
          </SwiperSlide>
          <SwiperSlide>
            <div className={css.bannerImg}>
              <img src={people} alt="people are on a hike" />
            </div>
            <BannerInfo />
          </SwiperSlide>
          <SwiperSlide>
            <div className={css.bannerImg}>
              <img src={tent} alt="tent" />
            </div>
            <BannerInfo />
          </SwiperSlide>
          <div className={css.swiperButton}>
            <div
              id="BannerBtnPrev"
              className={`BannerBtnPrev ${css.swiperButtonPrev}`}
            />
            <div
              id="BannerBtnNext"
              className={`BannerBtnNext ${css.swiperButtonNext}`}
            />
          </div>
          <div id="Banner" className={css.swiperPagination}>
            <span id="Banner" className={css.swiperPaginationBullet} />
          </div>
        </Swiper>
      </div>

      <div className={css.banner}>
        <div className={css.bannerImg}>
          <img src={mountainView} alt="mountain" />
          <img src={people} alt="people are on a hike" />
          <img src={tent} alt="tent" />
        </div>
        <BannerInfo />
      </div>
    </>
  );
};

export { Banner };
