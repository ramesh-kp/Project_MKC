import { graphql } from "@keystone-6/core";
import { virtual } from "@keystone-6/core/fields";
import { KeystoneContext } from "@keystone-6/core/types";

const avgResolverGen =
  (deviceConditionId: string) =>
  async (
    item: any,
    all: { from: Date; to: Date },
    context: KeystoneContext
  ) => {
    const device: { [key: string]: string } = {};
    device[deviceConditionId] = item.id;
    const result = await context.prisma.deviceRead.aggregate({
      _avg: {
        value: true,
      },
      where: {
        createdAt: {
          gte: new Date(all.from),
          lte: new Date(all.to),
        },
        device,
      },
    });
    return result?._avg?.value || (0 as number);
  };
export const avgField = (deviceConditionId: string) =>
  virtual({
    field: graphql.field({
      type: graphql.Float,
      args: {
        from: graphql.arg({
          type: graphql.nonNull(graphql.DateTime),
          defaultValue: new Date(
            new Date().getTime() - 1000 * 60 * 60 * 24 * 7
          ),
        }),
        to: graphql.arg({
          type: graphql.nonNull(graphql.DateTime),
          defaultValue: new Date(),
        }),
      },
      resolve: avgResolverGen(deviceConditionId),
    }),
  });
