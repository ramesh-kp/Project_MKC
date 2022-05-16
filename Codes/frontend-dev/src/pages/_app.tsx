import { useState } from 'react';
import Head from 'next/head';
import type { AppProps } from 'next/app';
import { Hydrate, QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { SessionLoader } from '../domain/lib/useSession';
import { BaseAppLayout } from '../components/AppLayout/BaseLayout';
import favicon from '../../public/favicon.ico';
import '../../styles/globals.css';

function MyApp({ Component, pageProps }: AppProps) {
  const [queryClient] = useState(() => new QueryClient());
  return (
    <>
      <Head>
        <link rel="shortcut icon" href={favicon.src} type="image/x-icon" />
        <title>Markaz Knowledge City</title>
      </Head>
      <QueryClientProvider client={queryClient}>
        <Hydrate state={pageProps.dehydratedState}>
          <SessionLoader>
            <BaseAppLayout>
              <Component {...pageProps} />
            </BaseAppLayout>
          </SessionLoader>
        </Hydrate>
        {process.env.NODE_ENV === 'development' && (
          <ReactQueryDevtools initialIsOpen={false} />
        )}
      </QueryClientProvider>
    </>
  );
}

export default MyApp;
