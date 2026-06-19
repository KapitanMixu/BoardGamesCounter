from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "wishlist_items" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "planszeo_url" VARCHAR(500),
    "bgg_url" VARCHAR(500),
    "notes" TEXT,
    "best_price" DOUBLE PRECISION,
    "best_price_shop" VARCHAR(255),
    "offer_count" INT,
    "price_updated_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "wishlist_items";"""


MODELS_STATE = (
    "eJztW21z2jgQ/isMn9KZXCdwSdu5b0CclmsCGSDXTjsdj7CF8cRIri2XcB3++0myjSwju5"
    "jyYg5/C6tdS/tI2n1WUn7WZ9iEjv/6PZjB+l+1n3UU/iHJL2t14LpCygQEjB2uaFENLgFj"
    "n3jAIFQ4AY4PqciEvuHZLrExolIUOA4TYoMq2sgSogDZ3wOoE2xBMoUebfj6jYptZMIX+v"
    "Hop/usT2zomNI4bZP1zeU6Wbhc1kXkjiuy3sa6gZ1ghoSyuyBTjFbaNiJMakEEPUAg+zzx"
    "AjZ8NrrIzdijcKRCJRxiwsaEExA4JOHuhhgYGDH86Gh87qDFevmj2bh+e/3uzzfX76gKH8"
    "lK8nYZuid8Dw05Ar1RfcnbAQGhBodR4IaiiZWR60yBp4Yu1k+BR4ecBi+GKg+9WCDgE0tm"
    "R/jNwIvuQGSRKQPt5iYHrX9ag86H1uCCar1i3mC6jMPF3YuammEbgzSxRWykuw5YQM8vsA"
    "ZTVr9ejLvCs3nsxZhAjs7NFsjJVodD7ro8yJkBdY6OQafLKCCwCHwq060wjCLdITfzvlDk"
    "jheIgmuGW4XDIwAoR8OrTYLhVXYsvEqHwrFl6YHnFIEyYXKSIN5cbYIi1cqEkbfJOBoeZB"
    "7rgKxDeUtbiD2DajhlyxSiZmT6Ov6jpDmb+mD2kbOIpjcH31H3QRuOWg+PzJOZ7393OESt"
    "kcZamly6SEkv3qSmYvWR2qfu6EON/ax96fc0jiD2ieXxHoXe6EudjQkEBOsIz3VgJphfLI"
    "2BWTLOOnlOsC8mGAPjeQ48U5daxArwoe9T2BSBvR1Z3n0cQIdHIcVMJ2j7MPxSOad6Ga/f"
    "WCqmXGABX1yAdoCGFn/nxLBg6wU3cdYKWm+aNWdpCUDA4qNmfbOeIkweOZGqK0q+qOUyr+"
    "hL0LCq7Csf06nKvj2WfVWOPvscbWBPVXoVyUlD9o1yTvFR8lGSsWScQyYITf5xpJ4kUVV+"
    "qvJTSUvIvaQnTs22yU6SYZWcSpCcktOKsPK0bwRfMoLKyuBEtkbeXGmfR9I0xRvg4qH1+Z"
    "U0Vff93vtYPbFhOvf9dmqf8ERRKEwnLA539nz8cL1GkWQM1wG8o8zGttBHuOA4dumIADJU"
    "YTp1yVg+/LKoEBV7YL7K+8mlQd2jTkESJq7WsNO61erLilYeh1aGeCgI5QqobCop5qPikG"
    "ULSnkc0sW8p82xEwZneh82txEKj/xSkQdjBwKkRk0YpVAbU6t9haCi229zktHu9+8lktHu"
    "plnE00NbG1w0OOOgSnYY49fhDE9Hi5ELyeac6EUSuKhuL4acbHRO0OUwM1+cleyAnJ3kVV"
    "Kao8nrRE3T1nfxDhAUFyqnC54UnopS3H0SPHG3pyB50sVfNtGT7xkrsle2OJdH9qoLrd8+"
    "MaxOQqqTkDKchOwzTXyy/alj+6RL4EyVKaT23GQxjzR1Sv9nVcKoEkbJNuphrpiQ/y/ERZ"
    "98pu1O5GbiAO8+q/ezu8GxuiXb8S3ZGNJM53q2oWI3DgYZsMpmKWwnzO7U0L3tP7Xvtdrj"
    "QOt0h91+T74g5o3yseBAa91ngqn7U+wW2u3rpieyYg+Qj/BkAj0KVoAUjx4yOVHK6kyP/s"
    "M1Fbjmlm8aVfY7eDxSqr1fprcisdu5j0WqJ6r/o1dABZ6o7rOCbkG606d1Re0ctVzmVc1A"
    "6FTVcunSQXa1/AN66nukbKqSMKlq5hWQbGsUADFSP00AGxuVdo2c0q6h+NdIjAhUEby/h/"
    "1eRjITJikgnxB18KtpG+Syxg7zvpUT1hwUmdf51V66sEtlI/aBtupQ+5DpZfkfT5v5tA=="
)
