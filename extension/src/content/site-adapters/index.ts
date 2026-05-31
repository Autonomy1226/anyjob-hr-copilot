// Site adapter registry — selects the correct adapter based on hostname

import type { SiteAdapter } from './base.adapter'
import { BosszhipinAdapter } from './bosszhipin.adapter'
import { LiepinAdapter } from './liepin.adapter'
import { ZhaopinAdapter } from './zhaopin.adapter'
import { LocalTestAdapter } from './local.adapter'

export function getAdapterForSite(hostname: string): SiteAdapter | null {
  if (hostname.includes('zhipin.com')) {
    return new BosszhipinAdapter()
  }
  if (hostname.includes('liepin.com')) {
    return new LiepinAdapter()
  }
  if (hostname.includes('zhaopin.com')) {
    return new ZhaopinAdapter()
  }
  if (hostname.includes('localhost') || hostname.includes('127.0.0.1')) {
    return new LocalTestAdapter()
  }
  return null
}

export type { SiteAdapter } from './base.adapter'
